import os
from ..models.S3Operation import S3Operation
from ..enums.S3OperationType import S3OperationType
from ..enums.S3OperationStatus import S3OperationStatus
from ..factory.S3StrategyFactory import S3StrategyFactory

class S3Service:
    def __init__(self, operation_repository, aws_access_key=None, aws_secret_key=None, region_name=None):
        """
        Initialize the S3 service.
        
        Args:
            operation_repository: Repository for storing operation information
            aws_access_key: AWS access key ID (optional, can use environment variables)
            aws_secret_key: AWS secret access key (optional, can use environment variables)
            region_name: AWS region name (optional, can use environment variables)
        """
        self.operation_repository = operation_repository
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.active_operations = {}  # Dictionary of operation_id -> strategy
    
    def create_upload_operation(self, local_file_path, bucket_name, object_key):
        """
        Create a new upload operation.
        
        Args:
            local_file_path: Path to the local file to upload
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            str: The ID of the created operation
        """
        # Create operation object
        operation = S3Operation(
            operation_type=S3OperationType.UPLOAD,
            bucket_name=bucket_name,
            object_key=object_key,
            local_file_path=local_file_path
        )
        
        # Save to repository
        self.operation_repository.save_operation(operation)
        
        return operation.id
    
    def create_download_operation(self, bucket_name, object_key, local_file_path):
        """
        Create a new download operation.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            local_file_path: Path where the file should be saved locally
            
        Returns:
            str: The ID of the created operation
        """
        # Create operation object
        operation = S3Operation(
            operation_type=S3OperationType.DOWNLOAD,
            bucket_name=bucket_name,
            object_key=object_key,
            local_file_path=local_file_path
        )
        
        # Save to repository
        self.operation_repository.save_operation(operation)
        
        return operation.id
    
    def create_delete_operation(self, bucket_name, object_key):
        """
        Create a new delete operation.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            str: The ID of the created operation
        """
        # Create operation object
        operation = S3Operation(
            operation_type=S3OperationType.DELETE,
            bucket_name=bucket_name,
            object_key=object_key
        )
        
        # Save to repository
        self.operation_repository.save_operation(operation)
        
        return operation.id
    
    def create_copy_operation(self, source_bucket, source_key, dest_bucket, dest_key):
        """
        Create a new copy operation.
        
        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
            
        Returns:
            str: The ID of the created operation
        """
        # Create operation object
        operation = S3Operation(
            operation_type=S3OperationType.COPY,
            bucket_name=source_bucket,
            object_key=source_key,
            destination_bucket=dest_bucket,
            destination_key=dest_key
        )
        
        # Save to repository
        self.operation_repository.save_operation(operation)
        
        return operation.id
    
    def start_operation(self, operation_id, strategy_type="standard"):
        """
        Start an S3 operation by its ID.
        
        Args:
            operation_id: The ID of the operation to start
            strategy_type: The type of S3 strategy to use ('standard' or 'multipart')
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        # Get operation from repository
        operation = self.operation_repository.get_operation(operation_id)
        if not operation:
            return False
        
        # Check if operation is already in progress
        if operation_id in self.active_operations:
            return False
        
        # Create appropriate S3 strategy
        strategy = S3StrategyFactory.create_strategy(
            strategy_type=strategy_type,
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            region_name=self.region_name
        )
        
        # Start operation based on type
        result = False
        
        if operation.operation_type == S3OperationType.UPLOAD:
            # Start upload
            result = strategy.upload(
                operation.local_file_path,
                operation.bucket_name,
                operation.object_key,
                callback=lambda transferred_size=None, file_size=None, error=None: 
                    self._update_progress(operation_id, transferred_size, file_size, error)
            )
        
        elif operation.operation_type == S3OperationType.DOWNLOAD:
            # Start download
            result = strategy.download(
                operation.bucket_name,
                operation.object_key,
                operation.local_file_path,
                callback=lambda transferred_size=None, file_size=None, error=None: 
                    self._update_progress(operation_id, transferred_size, file_size, error)
            )
        
        elif operation.operation_type == S3OperationType.DELETE:
            # Start delete
            result = strategy.delete(
                operation.bucket_name,
                operation.object_key,
                callback=lambda transferred_size=None, file_size=None, error=None: 
                    self._update_progress(operation_id, transferred_size, file_size, error)
            )
        
        elif operation.operation_type == S3OperationType.COPY:
            # Start copy
            result = strategy.copy(
                operation.bucket_name,
                operation.object_key,
                operation.destination_bucket,
                operation.destination_key,
                callback=lambda transferred_size=None, file_size=None, error=None: 
                    self._update_progress(operation_id, transferred_size, file_size, error)
            )
        
        if result:
            # Update operation status
            operation.start()
            self.operation_repository.save_operation(operation)
            
            # Store active operation
            self.active_operations[operation_id] = strategy
        
        return result
    
    def cancel_operation(self, operation_id):
        """
        Cancel an S3 operation by its ID.
        
        Args:
            operation_id: The ID of the operation to cancel
            
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if operation_id not in self.active_operations:
            return False
        
        strategy = self.active_operations[operation_id]
        result = strategy.cancel()
        
        if result:
            # Update operation status
            operation = self.operation_repository.get_operation(operation_id)
            if operation:
                operation.cancel()
                self.operation_repository.save_operation(operation)
            
            # Remove from active operations
            del self.active_operations[operation_id]
        
        return result
    
    def get_operation(self, operation_id):
        """
        Get an operation by its ID.
        
        Args:
            operation_id: The ID of the operation to get
            
        Returns:
            S3Operation: The operation object, or None if not found
        """
        return self.operation_repository.get_operation(operation_id)
    
    def get_all_operations(self):
        """
        Get all operations.
        
        Returns:
            list: List of all operation objects
        """
        return self.operation_repository.get_all_operations()
    
    def list_objects(self, bucket_name, prefix=None):
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Optional prefix to filter objects
            
        Returns:
            list: List of object keys in the bucket
        """
        # Create a temporary strategy for listing objects
        strategy = S3StrategyFactory.create_strategy(
            aws_access_key=self.aws_access_key,
            aws_secret_key=self.aws_secret_key,
            region_name=self.region_name
        )
        
        return strategy.list_objects(bucket_name, prefix)
    
    def _update_progress(self, operation_id, transferred_size, file_size, error):
        """
        Update operation progress (callback for S3 strategies).
        
        Args:
            operation_id: The ID of the operation
            transferred_size: The number of bytes transferred
            file_size: The total file size in bytes
            error: Error message if operation failed
        """
        operation = self.operation_repository.get_operation(operation_id)
        if not operation:
            return
        
        if error:
            # Handle operation error
            operation.fail(error)
            if operation_id in self.active_operations:
                del self.active_operations[operation_id]
        elif transferred_size is not None:
            # Update progress
            operation.update_progress(transferred_size, file_size)
            
            # Check if operation is complete
            if file_size and transferred_size >= file_size:
                operation.complete()
                if operation_id in self.active_operations:
                    del self.active_operations[operation_id]
        
        # Save updated operation
        self.operation_repository.save_operation(operation)

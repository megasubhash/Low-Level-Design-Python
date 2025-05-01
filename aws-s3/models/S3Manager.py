from collections import defaultdict
from ..enums.S3OperationStatus import S3OperationStatus

class S3Manager:
    def __init__(self, s3_service):
        """
        Initialize the S3Manager.
        
        Args:
            s3_service: The service to handle S3 operations
        """
        self.s3_service = s3_service
        self.operations = {}  # Dictionary of all operations by ID
        self.operations_by_status = defaultdict(list)  # Group operations by status
    
    def upload_file(self, local_file_path, bucket_name, object_key):
        """
        Upload a file to an S3 bucket.
        
        Args:
            local_file_path: Path to the local file to upload
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            str: The ID of the created operation
        """
        operation_id = self.s3_service.create_upload_operation(local_file_path, bucket_name, object_key)
        operation = self.s3_service.get_operation(operation_id)
        
        self.operations[operation_id] = operation
        self.operations_by_status[operation.status.value].append(operation_id)
        
        return operation_id
    
    def download_file(self, bucket_name, object_key, local_file_path):
        """
        Download a file from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            local_file_path: Path where the file should be saved locally
            
        Returns:
            str: The ID of the created operation
        """
        operation_id = self.s3_service.create_download_operation(bucket_name, object_key, local_file_path)
        operation = self.s3_service.get_operation(operation_id)
        
        self.operations[operation_id] = operation
        self.operations_by_status[operation.status.value].append(operation_id)
        
        return operation_id
    
    def delete_object(self, bucket_name, object_key):
        """
        Delete an object from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            str: The ID of the created operation
        """
        operation_id = self.s3_service.create_delete_operation(bucket_name, object_key)
        operation = self.s3_service.get_operation(operation_id)
        
        self.operations[operation_id] = operation
        self.operations_by_status[operation.status.value].append(operation_id)
        
        return operation_id
    
    def list_objects(self, bucket_name, prefix=None):
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Optional prefix to filter objects
            
        Returns:
            list: List of object keys in the bucket
        """
        return self.s3_service.list_objects(bucket_name, prefix)
    
    def copy_object(self, source_bucket, source_key, dest_bucket, dest_key):
        """
        Copy an object from one location to another in S3.
        
        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
            
        Returns:
            str: The ID of the created operation
        """
        operation_id = self.s3_service.create_copy_operation(source_bucket, source_key, dest_bucket, dest_key)
        operation = self.s3_service.get_operation(operation_id)
        
        self.operations[operation_id] = operation
        self.operations_by_status[operation.status.value].append(operation_id)
        
        return operation_id
    
    def start_operation(self, operation_id):
        """
        Start an S3 operation by its ID.
        
        Args:
            operation_id: The ID of the operation to start
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        # Update status tracking
        old_status = operation.status
        result = self.s3_service.start_operation(operation_id)
        
        if result and operation.status != old_status:
            self.operations_by_status[old_status.value].remove(operation_id)
            self.operations_by_status[operation.status.value].append(operation_id)
        
        return result
    
    def cancel_operation(self, operation_id):
        """
        Cancel an S3 operation by its ID.
        
        Args:
            operation_id: The ID of the operation to cancel
            
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if operation_id not in self.operations:
            return False
        
        operation = self.operations[operation_id]
        
        # Update status tracking
        old_status = operation.status
        result = self.s3_service.cancel_operation(operation_id)
        
        if result and operation.status != old_status:
            self.operations_by_status[old_status.value].remove(operation_id)
            self.operations_by_status[operation.status.value].append(operation_id)
        
        return result
    
    def get_operation(self, operation_id):
        """
        Get an operation by its ID.
        
        Args:
            operation_id: The ID of the operation to get
            
        Returns:
            S3Operation: The operation object, or None if not found
        """
        return self.operations.get(operation_id)
    
    def get_all_operations(self):
        """
        Get all operations.
        
        Returns:
            list: List of all operation objects
        """
        return list(self.operations.values())
    
    def get_operations_by_status(self, status):
        """
        Get all operations with a specific status.
        
        Args:
            status: The status to filter by (S3OperationStatus enum)
            
        Returns:
            list: List of operation objects with the specified status
        """
        operation_ids = self.operations_by_status[status.value]
        return [self.operations[operation_id] for operation_id in operation_ids]
    
    def __str__(self):
        status_counts = {status.value: len(ids) for status, ids in self.operations_by_status.items()}
        return f"S3Manager(total_operations={len(self.operations)}, status_counts={status_counts})"

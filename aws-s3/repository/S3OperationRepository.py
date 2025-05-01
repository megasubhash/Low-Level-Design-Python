import os
import json
import threading
from datetime import datetime
from ..models.S3Operation import S3Operation
from ..enums.S3OperationType import S3OperationType
from ..enums.S3OperationStatus import S3OperationStatus

class S3OperationRepository:
    def __init__(self, storage_path=None):
        """
        Initialize the S3 operation repository.
        
        Args:
            storage_path: Path to store operation information (default: ~/.aws_s3_manager)
        """
        if storage_path is None:
            home_dir = os.path.expanduser("~")
            storage_path = os.path.join(home_dir, ".aws_s3_manager")
        
        self.storage_path = storage_path
        self.operations_file = os.path.join(storage_path, "operations.json")
        self.lock = threading.Lock()  # For thread-safe operations
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    def save_operation(self, operation):
        """
        Save an operation to the repository.
        
        Args:
            operation: The S3Operation object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        with self.lock:
            try:
                # Load existing operations
                operations = self._load_operations()
                
                # Convert S3Operation object to dictionary
                operation_dict = {
                    'id': operation.id,
                    'operation_type': operation.operation_type.value,
                    'bucket_name': operation.bucket_name,
                    'object_key': operation.object_key,
                    'local_file_path': operation.local_file_path,
                    'destination_bucket': operation.destination_bucket,
                    'destination_key': operation.destination_key,
                    'status': operation.status.value,
                    'progress': operation.progress,
                    'created_at': operation.created_at.isoformat() if operation.created_at else None,
                    'started_at': operation.started_at.isoformat() if operation.started_at else None,
                    'completed_at': operation.completed_at.isoformat() if operation.completed_at else None,
                    'file_size': operation.file_size,
                    'transferred_size': operation.transferred_size,
                    'error_message': operation.error_message
                }
                
                # Update or add operation
                operations[operation.id] = operation_dict
                
                # Save to file
                return self._save_operations(operations)
            
            except Exception as e:
                print(f"Error saving operation: {str(e)}")
                return False
    
    def get_operation(self, operation_id):
        """
        Get an operation from the repository by ID.
        
        Args:
            operation_id: The ID of the operation to get
            
        Returns:
            S3Operation: The operation object, or None if not found
        """
        with self.lock:
            try:
                operations = self._load_operations()
                operation_dict = operations.get(operation_id)
                
                if operation_dict:
                    return self._dict_to_operation(operation_dict)
                
                return None
            
            except Exception as e:
                print(f"Error getting operation: {str(e)}")
                return None
    
    def get_all_operations(self):
        """
        Get all operations from the repository.
        
        Returns:
            list: List of all operation objects
        """
        with self.lock:
            try:
                operations = self._load_operations()
                return [self._dict_to_operation(operation_dict) for operation_dict in operations.values()]
            
            except Exception as e:
                print(f"Error getting all operations: {str(e)}")
                return []
    
    def delete_operation(self, operation_id):
        """
        Delete an operation from the repository.
        
        Args:
            operation_id: The ID of the operation to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        with self.lock:
            try:
                operations = self._load_operations()
                
                if operation_id in operations:
                    del operations[operation_id]
                    return self._save_operations(operations)
                
                return False
            
            except Exception as e:
                print(f"Error deleting operation: {str(e)}")
                return False
    
    def _load_operations(self):
        """Load operations from the storage file."""
        if not os.path.exists(self.operations_file):
            return {}
        
        try:
            with open(self.operations_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_operations(self, operations):
        """Save operations to the storage file."""
        try:
            with open(self.operations_file, 'w') as f:
                json.dump(operations, f, indent=2)
            return True
        except:
            return False
    
    def _dict_to_operation(self, operation_dict):
        """Convert a dictionary to an S3Operation object."""
        from datetime import datetime
        
        operation = S3Operation(
            operation_type=S3OperationType(operation_dict['operation_type']),
            bucket_name=operation_dict['bucket_name'],
            object_key=operation_dict['object_key'],
            local_file_path=operation_dict.get('local_file_path'),
            destination_bucket=operation_dict.get('destination_bucket'),
            destination_key=operation_dict.get('destination_key')
        )
        
        # Set ID and other properties
        operation.id = operation_dict['id']
        operation.status = S3OperationStatus(operation_dict['status'])
        operation.progress = operation_dict['progress']
        operation.file_size = operation_dict['file_size']
        operation.transferred_size = operation_dict['transferred_size']
        operation.error_message = operation_dict.get('error_message')
        
        # Parse datetime strings
        if operation_dict.get('created_at'):
            operation.created_at = datetime.fromisoformat(operation_dict['created_at'])
        if operation_dict.get('started_at'):
            operation.started_at = datetime.fromisoformat(operation_dict['started_at'])
        if operation_dict.get('completed_at'):
            operation.completed_at = datetime.fromisoformat(operation_dict['completed_at'])
        
        return operation

import uuid
from datetime import datetime
from ..enums.S3OperationType import S3OperationType
from ..enums.S3OperationStatus import S3OperationStatus

class S3Operation:
    def __init__(self, operation_type, bucket_name, object_key, local_file_path=None, destination_bucket=None, destination_key=None):
        """
        Initialize a new S3Operation object.
        
        Args:
            operation_type: Type of S3 operation (S3OperationType enum)
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            local_file_path: Path to the local file (for upload/download operations)
            destination_bucket: Destination bucket name (for copy operations)
            destination_key: Destination object key (for copy operations)
        """
        self.id = str(uuid.uuid4())
        self.operation_type = operation_type
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.local_file_path = local_file_path
        self.destination_bucket = destination_bucket
        self.destination_key = destination_key
        self.status = S3OperationStatus.PENDING
        self.progress = 0.0
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.file_size = 0
        self.transferred_size = 0
        self.error_message = None
    
    def start(self):
        """Mark the operation as started."""
        self.status = S3OperationStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete(self):
        """Mark the operation as completed."""
        self.status = S3OperationStatus.COMPLETED
        self.progress = 100.0
        self.completed_at = datetime.now()
    
    def fail(self, error_message):
        """Mark the operation as failed with an error message."""
        self.status = S3OperationStatus.FAILED
        self.error_message = error_message
    
    def cancel(self):
        """Mark the operation as cancelled."""
        self.status = S3OperationStatus.CANCELLED
    
    def update_progress(self, transferred_size, file_size=None):
        """Update the operation progress."""
        self.transferred_size = transferred_size
        if file_size:
            self.file_size = file_size
        
        if self.file_size > 0:
            self.progress = (self.transferred_size / self.file_size) * 100
    
    def __str__(self):
        return f"S3Operation(id={self.id}, type={self.operation_type.value}, bucket={self.bucket_name}, key={self.object_key}, status={self.status.value}, progress={self.progress:.1f}%)"

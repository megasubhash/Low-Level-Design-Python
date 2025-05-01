import os
import boto3
import threading
from botocore.exceptions import ClientError
from ..interfaces.IS3Strategy import IS3Strategy

class StandardS3Strategy(IS3Strategy):
    def __init__(self, aws_access_key=None, aws_secret_key=None, region_name=None):
        """
        Initialize the standard S3 strategy.
        
        Args:
            aws_access_key: AWS access key ID (optional, can use environment variables)
            aws_secret_key: AWS secret access key (optional, can use environment variables)
            region_name: AWS region name (optional, can use environment variables)
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.s3_client = None
        self.current_operation = None
        self.progress = 0.0
        self.transferred_bytes = 0
        self.total_bytes = 0
        self.is_cancelled = False
        self.operation_thread = None
        self.callback = None
    
    def _initialize_client(self):
        """Initialize the S3 client if not already initialized."""
        if self.s3_client is None:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region_name
            )
            self.s3_client = session.client('s3')
    
    def upload(self, local_file_path, bucket_name, object_key, callback=None):
        """
        Upload a file to an S3 bucket.
        
        Args:
            local_file_path: Path to the local file to upload
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            callback: Optional callback function for progress updates
            
        Returns:
            bool: True if upload started successfully, False otherwise
        """
        self._initialize_client()
        self.callback = callback
        self.is_cancelled = False
        self.progress = 0.0
        self.transferred_bytes = 0
        
        # Get file size
        try:
            self.total_bytes = os.path.getsize(local_file_path)
        except:
            self.total_bytes = 0
        
        # Start upload in a separate thread
        self.operation_thread = threading.Thread(
            target=self._upload_thread,
            args=(local_file_path, bucket_name, object_key)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
        
        return True
    
    def _upload_thread(self, local_file_path, bucket_name, object_key):
        """Internal method to handle the upload process in a separate thread."""
        try:
            # Create a callback for upload progress
            def s3_upload_progress(bytes_transferred):
                if self.is_cancelled:
                    raise Exception("Operation cancelled")
                
                self.transferred_bytes = bytes_transferred
                if self.total_bytes > 0:
                    self.progress = (bytes_transferred / self.total_bytes) * 100
                
                if self.callback:
                    self.callback(bytes_transferred, self.total_bytes)
            
            # Upload file with progress tracking
            self.s3_client.upload_file(
                local_file_path,
                bucket_name,
                object_key,
                Callback=s3_upload_progress
            )
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.total_bytes, self.total_bytes)
        
        except Exception as e:
            # Handle upload errors
            if self.callback:
                self.callback(error=str(e))
    
    def download(self, bucket_name, object_key, local_file_path, callback=None):
        """
        Download a file from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            local_file_path: Path where the file should be saved locally
            callback: Optional callback function for progress updates
            
        Returns:
            bool: True if download started successfully, False otherwise
        """
        self._initialize_client()
        self.callback = callback
        self.is_cancelled = False
        self.progress = 0.0
        self.transferred_bytes = 0
        
        # Get object size
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            self.total_bytes = response.get('ContentLength', 0)
        except:
            self.total_bytes = 0
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        # Start download in a separate thread
        self.operation_thread = threading.Thread(
            target=self._download_thread,
            args=(bucket_name, object_key, local_file_path)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
        
        return True
    
    def _download_thread(self, bucket_name, object_key, local_file_path):
        """Internal method to handle the download process in a separate thread."""
        try:
            # Create a callback for download progress
            def s3_download_progress(bytes_transferred):
                if self.is_cancelled:
                    raise Exception("Operation cancelled")
                
                self.transferred_bytes = bytes_transferred
                if self.total_bytes > 0:
                    self.progress = (bytes_transferred / self.total_bytes) * 100
                
                if self.callback:
                    self.callback(bytes_transferred, self.total_bytes)
            
            # Download file with progress tracking
            self.s3_client.download_file(
                bucket_name,
                object_key,
                local_file_path,
                Callback=s3_download_progress
            )
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.total_bytes, self.total_bytes)
        
        except Exception as e:
            # Handle download errors
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            
            if self.callback:
                self.callback(error=str(e))
    
    def delete(self, bucket_name, object_key, callback=None):
        """
        Delete an object from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            callback: Optional callback function for status updates
            
        Returns:
            bool: True if deletion started successfully, False otherwise
        """
        self._initialize_client()
        self.callback = callback
        self.is_cancelled = False
        
        # Start delete in a separate thread
        self.operation_thread = threading.Thread(
            target=self._delete_thread,
            args=(bucket_name, object_key)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
        
        return True
    
    def _delete_thread(self, bucket_name, object_key):
        """Internal method to handle the delete process in a separate thread."""
        try:
            if self.is_cancelled:
                raise Exception("Operation cancelled")
            
            # Delete object
            self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(1, 1)  # Indicate completion
        
        except Exception as e:
            # Handle delete errors
            if self.callback:
                self.callback(error=str(e))
    
    def list_objects(self, bucket_name, prefix=None):
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Optional prefix to filter objects
            
        Returns:
            list: List of object keys in the bucket
        """
        self._initialize_client()
        
        try:
            # List objects in the bucket
            if prefix:
                response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            else:
                response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            
            # Extract object keys
            objects = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append(obj['Key'])
            
            return objects
        
        except Exception as e:
            print(f"Error listing objects: {str(e)}")
            return []
    
    def copy(self, source_bucket, source_key, dest_bucket, dest_key, callback=None):
        """
        Copy an object from one location to another in S3.
        
        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
            callback: Optional callback function for status updates
            
        Returns:
            bool: True if copy started successfully, False otherwise
        """
        self._initialize_client()
        self.callback = callback
        self.is_cancelled = False
        self.progress = 0.0
        
        # Start copy in a separate thread
        self.operation_thread = threading.Thread(
            target=self._copy_thread,
            args=(source_bucket, source_key, dest_bucket, dest_key)
        )
        self.operation_thread.daemon = True
        self.operation_thread.start()
        
        return True
    
    def _copy_thread(self, source_bucket, source_key, dest_bucket, dest_key):
        """Internal method to handle the copy process in a separate thread."""
        try:
            if self.is_cancelled:
                raise Exception("Operation cancelled")
            
            # Copy object
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key
            )
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(1, 1)  # Indicate completion
        
        except Exception as e:
            # Handle copy errors
            if self.callback:
                self.callback(error=str(e))
    
    def cancel(self):
        """
        Cancel the current operation.
        
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if self.operation_thread and self.operation_thread.is_alive():
            self.is_cancelled = True
            return True
        return False
    
    def get_progress(self):
        """
        Get the current operation progress.
        
        Returns:
            float: Operation progress as a percentage (0-100)
        """
        return self.progress

import os
import boto3
import threading
from botocore.exceptions import ClientError
from ..interfaces.IS3Strategy import IS3Strategy

class MultipartS3Strategy(IS3Strategy):
    def __init__(self, aws_access_key=None, aws_secret_key=None, region_name=None, part_size_mb=5):
        """
        Initialize the multipart S3 strategy.
        
        Args:
            aws_access_key: AWS access key ID (optional, can use environment variables)
            aws_secret_key: AWS secret access key (optional, can use environment variables)
            region_name: AWS region name (optional, can use environment variables)
            part_size_mb: Size of each part in MB for multipart operations (default: 5)
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.part_size = part_size_mb * 1024 * 1024  # Convert to bytes
        self.s3_client = None
        self.progress = 0.0
        self.transferred_bytes = 0
        self.total_bytes = 0
        self.is_cancelled = False
        self.operation_thread = None
        self.callback = None
        self.upload_id = None
        self.parts = []
    
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
        Upload a file to an S3 bucket using multipart upload.
        
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
        self.parts = []
        
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
        """Internal method to handle the multipart upload process in a separate thread."""
        try:
            # Initiate multipart upload
            response = self.s3_client.create_multipart_upload(
                Bucket=bucket_name,
                Key=object_key
            )
            self.upload_id = response['UploadId']
            
            # Calculate number of parts
            file_size = os.path.getsize(local_file_path)
            num_parts = (file_size + self.part_size - 1) // self.part_size
            
            # Upload parts
            with open(local_file_path, 'rb') as file:
                for part_number in range(1, num_parts + 1):
                    if self.is_cancelled:
                        # Abort multipart upload if cancelled
                        self.s3_client.abort_multipart_upload(
                            Bucket=bucket_name,
                            Key=object_key,
                            UploadId=self.upload_id
                        )
                        raise Exception("Operation cancelled")
                    
                    # Calculate part size
                    start_byte = (part_number - 1) * self.part_size
                    end_byte = min(part_number * self.part_size, file_size)
                    part_size = end_byte - start_byte
                    
                    # Read part data
                    file.seek(start_byte)
                    part_data = file.read(part_size)
                    
                    # Upload part
                    response = self.s3_client.upload_part(
                        Bucket=bucket_name,
                        Key=object_key,
                        PartNumber=part_number,
                        UploadId=self.upload_id,
                        Body=part_data
                    )
                    
                    # Save ETag for part
                    self.parts.append({
                        'PartNumber': part_number,
                        'ETag': response['ETag']
                    })
                    
                    # Update progress
                    self.transferred_bytes = end_byte
                    self.progress = (end_byte / file_size) * 100
                    
                    if self.callback:
                        self.callback(self.transferred_bytes, self.total_bytes)
            
            # Complete multipart upload
            if not self.is_cancelled:
                self.s3_client.complete_multipart_upload(
                    Bucket=bucket_name,
                    Key=object_key,
                    UploadId=self.upload_id,
                    MultipartUpload={'Parts': self.parts}
                )
                
                # Set progress to 100% when complete
                self.progress = 100.0
                if self.callback:
                    self.callback(self.total_bytes, self.total_bytes)
        
        except Exception as e:
            # Abort multipart upload if it was initiated
            if self.upload_id:
                try:
                    self.s3_client.abort_multipart_upload(
                        Bucket=bucket_name,
                        Key=object_key,
                        UploadId=self.upload_id
                    )
                except:
                    pass
            
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
            # Get object size
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            file_size = response.get('ContentLength', 0)
            
            # Calculate number of parts
            num_parts = (file_size + self.part_size - 1) // self.part_size
            
            # Create empty file
            with open(local_file_path, 'wb') as file:
                pass
            
            # Download parts
            for part_number in range(1, num_parts + 1):
                if self.is_cancelled:
                    # Delete partial file if cancelled
                    if os.path.exists(local_file_path):
                        os.remove(local_file_path)
                    raise Exception("Operation cancelled")
                
                # Calculate part range
                start_byte = (part_number - 1) * self.part_size
                end_byte = min(part_number * self.part_size - 1, file_size - 1)
                
                # Download part
                response = self.s3_client.get_object(
                    Bucket=bucket_name,
                    Key=object_key,
                    Range=f'bytes={start_byte}-{end_byte}'
                )
                
                # Write part to file
                with open(local_file_path, 'r+b') as file:
                    file.seek(start_byte)
                    file.write(response['Body'].read())
                
                # Update progress
                self.transferred_bytes = end_byte + 1
                self.progress = (self.transferred_bytes / file_size) * 100
                
                if self.callback:
                    self.callback(self.transferred_bytes, self.total_bytes)
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.total_bytes, self.total_bytes)
        
        except Exception as e:
            # Delete partial file if there was an error
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            
            # Handle download errors
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
            
            # Get source object size
            response = self.s3_client.head_object(Bucket=source_bucket, Key=source_key)
            file_size = response.get('ContentLength', 0)
            
            # For small files, use simple copy
            if file_size < 5 * 1024 * 1024 * 1024:  # 5GB
                copy_source = {'Bucket': source_bucket, 'Key': source_key}
                self.s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket=dest_bucket,
                    Key=dest_key
                )
            else:
                # For large files, use multipart copy
                # Initiate multipart upload
                response = self.s3_client.create_multipart_upload(
                    Bucket=dest_bucket,
                    Key=dest_key
                )
                upload_id = response['UploadId']
                
                # Calculate number of parts
                num_parts = (file_size + self.part_size - 1) // self.part_size
                parts = []
                
                # Copy parts
                for part_number in range(1, num_parts + 1):
                    if self.is_cancelled:
                        # Abort multipart upload if cancelled
                        self.s3_client.abort_multipart_upload(
                            Bucket=dest_bucket,
                            Key=dest_key,
                            UploadId=upload_id
                        )
                        raise Exception("Operation cancelled")
                    
                    # Calculate part range
                    start_byte = (part_number - 1) * self.part_size
                    end_byte = min(part_number * self.part_size - 1, file_size - 1)
                    
                    # Copy part
                    copy_source = {
                        'Bucket': source_bucket,
                        'Key': source_key,
                        'Range': f'bytes={start_byte}-{end_byte}'
                    }
                    
                    response = self.s3_client.upload_part_copy(
                        Bucket=dest_bucket,
                        Key=dest_key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        CopySource=copy_source
                    )
                    
                    # Save ETag for part
                    parts.append({
                        'PartNumber': part_number,
                        'ETag': response['CopyPartResult']['ETag']
                    })
                    
                    # Update progress
                    self.transferred_bytes = end_byte + 1
                    self.progress = (self.transferred_bytes / file_size) * 100
                    
                    if self.callback:
                        self.callback(self.transferred_bytes, file_size)
                
                # Complete multipart upload
                if not self.is_cancelled:
                    self.s3_client.complete_multipart_upload(
                        Bucket=dest_bucket,
                        Key=dest_key,
                        UploadId=upload_id,
                        MultipartUpload={'Parts': parts}
                    )
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(file_size, file_size)
        
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

from abc import ABC, abstractmethod

class IS3Strategy(ABC):
    @abstractmethod
    def upload(self, local_file_path, bucket_name, object_key):
        """
        Upload a file to an S3 bucket.
        
        Args:
            local_file_path: Path to the local file to upload
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def download(self, bucket_name, object_key, local_file_path):
        """
        Download a file from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            local_file_path: Path where the file should be saved locally
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, bucket_name, object_key):
        """
        Delete an object from an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            object_key: Object key (path) in the S3 bucket
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_objects(self, bucket_name, prefix=None):
        """
        List objects in an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            prefix: Optional prefix to filter objects
            
        Returns:
            list: List of object keys in the bucket
        """
        pass
    
    @abstractmethod
    def copy(self, source_bucket, source_key, dest_bucket, dest_key):
        """
        Copy an object from one location to another in S3.
        
        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_progress(self):
        """
        Get the current operation progress.
        
        Returns:
            float: Operation progress as a percentage (0-100)
        """
        pass

import os
import json
import threading
from ..models.Download import Download
from ..enums.DownloadStatus import DownloadStatus

class DownloadRepository:
    def __init__(self, storage_path=None):
        """
        Initialize the download repository.
        
        Args:
            storage_path: Path to store download information (default: ~/.download_manager)
        """
        if storage_path is None:
            home_dir = os.path.expanduser("~")
            storage_path = os.path.join(home_dir, ".download_manager")
        
        self.storage_path = storage_path
        self.downloads_file = os.path.join(storage_path, "downloads.json")
        self.lock = threading.Lock()  # For thread-safe operations
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    def save_download(self, download):
        """
        Save a download to the repository.
        
        Args:
            download: The Download object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        with self.lock:
            try:
                # Load existing downloads
                downloads = self._load_downloads()
                
                # Convert Download object to dictionary
                download_dict = {
                    'id': download.id,
                    'url': download.url,
                    'destination_path': download.destination_path,
                    'file_name': download.file_name,
                    'status': download.status.value,
                    'progress': download.progress,
                    'created_at': download.created_at.isoformat() if download.created_at else None,
                    'started_at': download.started_at.isoformat() if download.started_at else None,
                    'completed_at': download.completed_at.isoformat() if download.completed_at else None,
                    'file_size': download.file_size,
                    'downloaded_size': download.downloaded_size,
                    'error_message': download.error_message
                }
                
                # Update or add download
                downloads[download.id] = download_dict
                
                # Save to file
                return self._save_downloads(downloads)
            
            except Exception as e:
                print(f"Error saving download: {str(e)}")
                return False
    
    def get_download(self, download_id):
        """
        Get a download from the repository by ID.
        
        Args:
            download_id: The ID of the download to get
            
        Returns:
            Download: The download object, or None if not found
        """
        with self.lock:
            try:
                downloads = self._load_downloads()
                download_dict = downloads.get(download_id)
                
                if download_dict:
                    return self._dict_to_download(download_dict)
                
                return None
            
            except Exception as e:
                print(f"Error getting download: {str(e)}")
                return None
    
    def get_all_downloads(self):
        """
        Get all downloads from the repository.
        
        Returns:
            list: List of all download objects
        """
        with self.lock:
            try:
                downloads = self._load_downloads()
                return [self._dict_to_download(download_dict) for download_dict in downloads.values()]
            
            except Exception as e:
                print(f"Error getting all downloads: {str(e)}")
                return []
    
    def delete_download(self, download_id):
        """
        Delete a download from the repository.
        
        Args:
            download_id: The ID of the download to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        with self.lock:
            try:
                downloads = self._load_downloads()
                
                if download_id in downloads:
                    del downloads[download_id]
                    return self._save_downloads(downloads)
                
                return False
            
            except Exception as e:
                print(f"Error deleting download: {str(e)}")
                return False
    
    def _load_downloads(self):
        """Load downloads from the storage file."""
        if not os.path.exists(self.downloads_file):
            return {}
        
        try:
            with open(self.downloads_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_downloads(self, downloads):
        """Save downloads to the storage file."""
        try:
            with open(self.downloads_file, 'w') as f:
                json.dump(downloads, f, indent=2)
            return True
        except:
            return False
    
    def _dict_to_download(self, download_dict):
        """Convert a dictionary to a Download object."""
        from datetime import datetime
        
        download = Download(
            url=download_dict['url'],
            destination_path=download_dict.get('destination_path'),
            file_name=download_dict.get('file_name')
        )
        
        # Set ID and other properties
        download.id = download_dict['id']
        download.status = DownloadStatus(download_dict['status'])
        download.progress = download_dict['progress']
        download.file_size = download_dict['file_size']
        download.downloaded_size = download_dict['downloaded_size']
        download.error_message = download_dict.get('error_message')
        
        # Parse datetime strings
        if download_dict.get('created_at'):
            download.created_at = datetime.fromisoformat(download_dict['created_at'])
        if download_dict.get('started_at'):
            download.started_at = datetime.fromisoformat(download_dict['started_at'])
        if download_dict.get('completed_at'):
            download.completed_at = datetime.fromisoformat(download_dict['completed_at'])
        
        return download

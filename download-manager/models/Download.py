import uuid
import os
from datetime import datetime
from ..enums.DownloadStatus import DownloadStatus

class Download:
    def __init__(self, url, destination_path=None, file_name=None):
        """
        Initialize a new Download object.
        
        Args:
            url: The URL to download from
            destination_path: The directory where the file should be saved (default: current directory)
            file_name: The name to save the file as (default: derived from URL)
        """
        self.id = str(uuid.uuid4())
        self.url = url
        self.destination_path = destination_path or os.getcwd()
        self.file_name = file_name or self._get_file_name_from_url(url)
        self.status = DownloadStatus.QUEUED
        self.progress = 0.0
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.file_size = 0
        self.downloaded_size = 0
        self.error_message = None
    
    def _get_file_name_from_url(self, url):
        """Extract filename from URL or generate a default one."""
        try:
            file_name = url.split('/')[-1]
            if not file_name or '?' in file_name:
                return f"download_{self.id[:8]}"
            return file_name
        except:
            return f"download_{self.id[:8]}"
    
    def get_full_path(self):
        """Get the full path where the file will be saved."""
        return os.path.join(self.destination_path, self.file_name)
    
    def update_progress(self, downloaded_size, file_size=None):
        """Update the download progress."""
        self.downloaded_size = downloaded_size
        if file_size:
            self.file_size = file_size
        
        if self.file_size > 0:
            self.progress = (self.downloaded_size / self.file_size) * 100
        
    def start(self):
        """Mark the download as started."""
        self.status = DownloadStatus.DOWNLOADING
        self.started_at = datetime.now()
    
    def pause(self):
        """Pause the download."""
        self.status = DownloadStatus.PAUSED
    
    def resume(self):
        """Resume the download."""
        self.status = DownloadStatus.DOWNLOADING
    
    def complete(self):
        """Mark the download as completed."""
        self.status = DownloadStatus.COMPLETED
        self.progress = 100.0
        self.completed_at = datetime.now()
    
    def fail(self, error_message):
        """Mark the download as failed with an error message."""
        self.status = DownloadStatus.FAILED
        self.error_message = error_message
    
    def __str__(self):
        return f"Download(id={self.id}, url={self.url}, status={self.status.value}, progress={self.progress:.1f}%)"

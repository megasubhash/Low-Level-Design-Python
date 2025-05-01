import os
import requests
import threading
from ..interfaces.IDownloadStrategy import IDownloadStrategy

class SimpleDownloadStrategy(IDownloadStrategy):
    def __init__(self):
        """Initialize the simple download strategy."""
        self.url = None
        self.destination_path = None
        self.is_paused = False
        self.is_cancelled = False
        self.progress = 0.0
        self.downloaded_size = 0
        self.file_size = 0
        self.download_thread = None
        self.callback = None
    
    def download(self, url, destination_path, callback=None):
        """
        Download a file from the given URL to the destination path.
        
        Args:
            url: The URL to download from
            destination_path: The path where the file should be saved
            callback: A function to call with progress updates
            
        Returns:
            bool: True if download started successfully, False otherwise
        """
        self.url = url
        self.destination_path = destination_path
        self.callback = callback
        self.is_paused = False
        self.is_cancelled = False
        
        # Start download in a separate thread
        self.download_thread = threading.Thread(target=self._download_thread)
        self.download_thread.daemon = True
        self.download_thread.start()
        
        return True
    
    def _download_thread(self):
        """Internal method to handle the download process in a separate thread."""
        try:
            # Make a HEAD request to get file size
            response = requests.head(self.url, allow_redirects=True)
            self.file_size = int(response.headers.get('content-length', 0))
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
            
            # Download the file
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                
                with open(self.destination_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.is_cancelled:
                            # Delete partial file if cancelled
                            f.close()
                            if os.path.exists(self.destination_path):
                                os.remove(self.destination_path)
                            return
                        
                        if self.is_paused:
                            # Wait while paused
                            while self.is_paused and not self.is_cancelled:
                                threading.Event().wait(0.1)
                            if self.is_cancelled:
                                continue
                        
                        # Write chunk to file
                        if chunk:
                            f.write(chunk)
                            self.downloaded_size += len(chunk)
                            self.progress = (self.downloaded_size / self.file_size * 100) if self.file_size > 0 else 0
                            
                            # Call progress callback if provided
                            if self.callback:
                                self.callback(self.downloaded_size, self.file_size)
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.file_size, self.file_size)
        
        except Exception as e:
            # Handle download errors
            if self.callback:
                self.callback(error=str(e))
    
    def pause(self):
        """
        Pause the current download.
        
        Returns:
            bool: True if paused successfully, False otherwise
        """
        if self.download_thread and self.download_thread.is_alive():
            self.is_paused = True
            return True
        return False
    
    def resume(self):
        """
        Resume a paused download.
        
        Returns:
            bool: True if resumed successfully, False otherwise
        """
        if self.download_thread and self.download_thread.is_alive() and self.is_paused:
            self.is_paused = False
            return True
        return False
    
    def cancel(self):
        """
        Cancel the current download.
        
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if self.download_thread and self.download_thread.is_alive():
            self.is_cancelled = True
            self.is_paused = False
            return True
        return False
    
    def get_progress(self):
        """
        Get the current download progress.
        
        Returns:
            float: Download progress as a percentage (0-100)
        """
        return self.progress

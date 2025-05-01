import os
import requests
import threading
import json
from ..interfaces.IDownloadStrategy import IDownloadStrategy

class ResumeDownloadStrategy(IDownloadStrategy):
    def __init__(self):
        """Initialize the resumable download strategy."""
        self.url = None
        self.destination_path = None
        self.metadata_path = None
        self.is_paused = False
        self.is_cancelled = False
        self.progress = 0.0
        self.downloaded_size = 0
        self.file_size = 0
        self.download_thread = None
        self.callback = None
    
    def download(self, url, destination_path, callback=None):
        """
        Download a file from the given URL to the destination path with resume capability.
        
        Args:
            url: The URL to download from
            destination_path: The path where the file should be saved
            callback: A function to call with progress updates
            
        Returns:
            bool: True if download started successfully, False otherwise
        """
        self.url = url
        self.destination_path = destination_path
        self.metadata_path = f"{destination_path}.metadata"
        self.callback = callback
        self.is_paused = False
        self.is_cancelled = False
        
        # Start download in a separate thread
        self.download_thread = threading.Thread(target=self._download_thread)
        self.download_thread.daemon = True
        self.download_thread.start()
        
        return True
    
    def _download_thread(self):
        """Internal method to handle the resumable download process."""
        try:
            # Check if we have existing metadata for this download
            start_byte = 0
            if os.path.exists(self.metadata_path) and os.path.exists(self.destination_path):
                try:
                    with open(self.metadata_path, 'r') as f:
                        metadata = json.load(f)
                        if metadata.get('url') == self.url:
                            start_byte = metadata.get('downloaded_size', 0)
                            self.downloaded_size = start_byte
                            self.file_size = metadata.get('file_size', 0)
                except:
                    # If metadata is corrupted, start from beginning
                    start_byte = 0
            
            # Make a HEAD request to get file size if we don't have it
            if self.file_size <= 0:
                response = requests.head(self.url, allow_redirects=True)
                self.file_size = int(response.headers.get('content-length', 0))
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
            
            # Set up headers for resuming download
            headers = {}
            file_mode = 'wb'
            
            if start_byte > 0 and start_byte < self.file_size:
                headers['Range'] = f'bytes={start_byte}-'
                file_mode = 'ab'  # Append to existing file
                
                # Update progress based on already downloaded data
                self.progress = (start_byte / self.file_size * 100) if self.file_size > 0 else 0
                if self.callback:
                    self.callback(start_byte, self.file_size)
            
            # Download the file
            with requests.get(self.url, headers=headers, stream=True) as response:
                response.raise_for_status()
                
                with open(self.destination_path, file_mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.is_cancelled:
                            # Don't delete the file if cancelled, as we can resume later
                            return
                        
                        if self.is_paused:
                            # Save metadata before pausing
                            self._save_metadata()
                            
                            # Wait while paused
                            while self.is_paused and not self.is_cancelled:
                                threading.Event().wait(0.1)
                            if self.is_cancelled:
                                return
                        
                        # Write chunk to file
                        if chunk:
                            f.write(chunk)
                            self.downloaded_size += len(chunk)
                            self.progress = (self.downloaded_size / self.file_size * 100) if self.file_size > 0 else 0
                            
                            # Call progress callback if provided
                            if self.callback:
                                self.callback(self.downloaded_size, self.file_size)
                            
                            # Periodically save metadata (every 1MB)
                            if self.downloaded_size % (1024 * 1024) < 8192:
                                self._save_metadata()
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.file_size, self.file_size)
                
                # Delete metadata file when download is complete
                if os.path.exists(self.metadata_path):
                    os.remove(self.metadata_path)
        
        except Exception as e:
            # Save metadata on error for later resuming
            self._save_metadata()
            
            # Handle download errors
            if self.callback:
                self.callback(error=str(e))
    
    def _save_metadata(self):
        """Save download metadata for resuming later."""
        metadata = {
            'url': self.url,
            'file_size': self.file_size,
            'downloaded_size': self.downloaded_size
        }
        
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f)
        except:
            pass  # Ignore metadata save errors
    
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
        elif not self.download_thread or not self.download_thread.is_alive():
            # If thread is not running, start a new one
            return self.download(self.url, self.destination_path, self.callback)
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

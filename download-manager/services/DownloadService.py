import os
from ..models.Download import Download
from ..enums.DownloadType import DownloadType
from ..enums.DownloadStatus import DownloadStatus
from ..factory.DownloadStrategyFactory import DownloadStrategyFactory

class DownloadService:
    def __init__(self, download_repository):
        """
        Initialize the download service.
        
        Args:
            download_repository: Repository for storing download information
        """
        self.download_repository = download_repository
        self.active_downloads = {}  # Dictionary of download_id -> strategy
    
    def create_download(self, url, destination_path=None, file_name=None, download_type=None):
        """
        Create a new download.
        
        Args:
            url: The URL to download from
            destination_path: The directory where the file should be saved
            file_name: The name to save the file as
            download_type: The type of download strategy to use
            
        Returns:
            Download: The created download object
        """
        # Create download object
        download = Download(url, destination_path, file_name)
        
        # Save to repository
        self.download_repository.save_download(download)
        
        return download
    
    def start_download(self, download_id, download_type=None):
        """
        Start a download by its ID.
        
        Args:
            download_id: The ID of the download to start
            download_type: The type of download strategy to use (optional)
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        # Get download from repository
        download = self.download_repository.get_download(download_id)
        if not download:
            return False
        
        # Check if download is already in progress
        if download_id in self.active_downloads:
            return False
        
        # Use specified download type or default to SIMPLE
        if download_type is None:
            download_type = DownloadType.SIMPLE
        
        # Create appropriate download strategy
        strategy = DownloadStrategyFactory.create_strategy(download_type)
        
        # Start download
        full_path = download.get_full_path()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Start download with progress callback
        result = strategy.download(
            download.url, 
            full_path, 
            callback=lambda downloaded_size=None, file_size=None, error=None: 
                self._update_progress(download_id, downloaded_size, file_size, error)
        )
        
        if result:
            # Update download status
            download.start()
            self.download_repository.save_download(download)
            
            # Store active download
            self.active_downloads[download_id] = strategy
        
        return result
    
    def pause_download(self, download_id):
        """
        Pause a download by its ID.
        
        Args:
            download_id: The ID of the download to pause
            
        Returns:
            bool: True if paused successfully, False otherwise
        """
        if download_id not in self.active_downloads:
            return False
        
        strategy = self.active_downloads[download_id]
        result = strategy.pause()
        
        if result:
            # Update download status
            download = self.download_repository.get_download(download_id)
            if download:
                download.pause()
                self.download_repository.save_download(download)
        
        return result
    
    def resume_download(self, download_id):
        """
        Resume a paused download by its ID.
        
        Args:
            download_id: The ID of the download to resume
            
        Returns:
            bool: True if resumed successfully, False otherwise
        """
        # Check if download is active but paused
        if download_id in self.active_downloads:
            strategy = self.active_downloads[download_id]
            result = strategy.resume()
            
            if result:
                # Update download status
                download = self.download_repository.get_download(download_id)
                if download:
                    download.resume()
                    self.download_repository.save_download(download)
            
            return result
        
        # If not active, start it again
        return self.start_download(download_id, DownloadType.RESUMABLE)
    
    def cancel_download(self, download_id):
        """
        Cancel a download by its ID.
        
        Args:
            download_id: The ID of the download to cancel
            
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if download_id not in self.active_downloads:
            return False
        
        strategy = self.active_downloads[download_id]
        result = strategy.cancel()
        
        if result:
            # Remove from active downloads
            del self.active_downloads[download_id]
            
            # Delete from repository
            self.download_repository.delete_download(download_id)
        
        return result
    
    def get_download_progress(self, download_id):
        """
        Get the progress of a download by its ID.
        
        Args:
            download_id: The ID of the download to get progress for
            
        Returns:
            float: Download progress as a percentage (0-100), or -1 if not found
        """
        if download_id in self.active_downloads:
            strategy = self.active_downloads[download_id]
            return strategy.get_progress()
        
        # Check repository for completed downloads
        download = self.download_repository.get_download(download_id)
        if download:
            return download.progress
        
        return -1
    
    def get_all_downloads(self):
        """
        Get all downloads.
        
        Returns:
            list: List of all download objects
        """
        return self.download_repository.get_all_downloads()
    
    def _update_progress(self, download_id, downloaded_size, file_size, error):
        """
        Update download progress (callback for download strategies).
        
        Args:
            download_id: The ID of the download
            downloaded_size: The number of bytes downloaded
            file_size: The total file size in bytes
            error: Error message if download failed
        """
        download = self.download_repository.get_download(download_id)
        if not download:
            return
        
        if error:
            # Handle download error
            download.fail(error)
            if download_id in self.active_downloads:
                del self.active_downloads[download_id]
        elif downloaded_size is not None:
            # Update progress
            download.update_progress(downloaded_size, file_size)
            
            # Check if download is complete
            if file_size and downloaded_size >= file_size:
                download.complete()
                if download_id in self.active_downloads:
                    del self.active_downloads[download_id]
        
        # Save updated download
        self.download_repository.save_download(download)

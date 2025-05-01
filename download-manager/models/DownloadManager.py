from collections import defaultdict
from ..enums.DownloadStatus import DownloadStatus

class DownloadManager:
    def __init__(self, download_service):
        """
        Initialize the DownloadManager.
        
        Args:
            download_service: The service to handle download operations
        """
        self.download_service = download_service
        self.downloads = {}  # Dictionary of all downloads by ID
        self.downloads_by_status = defaultdict(list)  # Group downloads by status
    
    def add_download(self, url, destination_path=None, file_name=None, download_type=None):
        """
        Add a new download to the manager.
        
        Args:
            url: The URL to download from
            destination_path: The directory where the file should be saved
            file_name: The name to save the file as
            download_type: The type of download strategy to use
            
        Returns:
            str: The ID of the created download
        """
        download = self.download_service.create_download(url, destination_path, file_name, download_type)
        self.downloads[download.id] = download
        self.downloads_by_status[download.status.value].append(download.id)
        return download.id
    
    def start_download(self, download_id):
        """
        Start a download by its ID.
        
        Args:
            download_id: The ID of the download to start
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        if download_id not in self.downloads:
            return False
        
        download = self.downloads[download_id]
        
        # Update status tracking
        old_status = download.status
        result = self.download_service.start_download(download_id)
        
        if result and download.status != old_status:
            self.downloads_by_status[old_status.value].remove(download_id)
            self.downloads_by_status[download.status.value].append(download_id)
        
        return result
    
    def pause_download(self, download_id):
        """
        Pause a download by its ID.
        
        Args:
            download_id: The ID of the download to pause
            
        Returns:
            bool: True if paused successfully, False otherwise
        """
        if download_id not in self.downloads:
            return False
        
        download = self.downloads[download_id]
        
        # Update status tracking
        old_status = download.status
        result = self.download_service.pause_download(download_id)
        
        if result and download.status != old_status:
            self.downloads_by_status[old_status.value].remove(download_id)
            self.downloads_by_status[download.status.value].append(download_id)
        
        return result
    
    def resume_download(self, download_id):
        """
        Resume a paused download by its ID.
        
        Args:
            download_id: The ID of the download to resume
            
        Returns:
            bool: True if resumed successfully, False otherwise
        """
        if download_id not in self.downloads:
            return False
        
        download = self.downloads[download_id]
        
        # Update status tracking
        old_status = download.status
        result = self.download_service.resume_download(download_id)
        
        if result and download.status != old_status:
            self.downloads_by_status[old_status.value].remove(download_id)
            self.downloads_by_status[download.status.value].append(download_id)
        
        return result
    
    def cancel_download(self, download_id):
        """
        Cancel a download by its ID.
        
        Args:
            download_id: The ID of the download to cancel
            
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if download_id not in self.downloads:
            return False
        
        download = self.downloads[download_id]
        
        # Update status tracking
        old_status = download.status
        result = self.download_service.cancel_download(download_id)
        
        if result:
            # Remove from status tracking and downloads list
            self.downloads_by_status[old_status.value].remove(download_id)
            del self.downloads[download_id]
        
        return result
    
    def get_download(self, download_id):
        """
        Get a download by its ID.
        
        Args:
            download_id: The ID of the download to get
            
        Returns:
            Download: The download object, or None if not found
        """
        return self.downloads.get(download_id)
    
    def get_all_downloads(self):
        """
        Get all downloads.
        
        Returns:
            list: List of all download objects
        """
        return list(self.downloads.values())
    
    def get_downloads_by_status(self, status):
        """
        Get all downloads with a specific status.
        
        Args:
            status: The status to filter by (DownloadStatus enum)
            
        Returns:
            list: List of download objects with the specified status
        """
        download_ids = self.downloads_by_status[status.value]
        return [self.downloads[download_id] for download_id in download_ids]
    
    def __str__(self):
        status_counts = {status.value: len(ids) for status, ids in self.downloads_by_status.items()}
        return f"DownloadManager(total_downloads={len(self.downloads)}, status_counts={status_counts})"

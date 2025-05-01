from abc import ABC, abstractmethod

class IDownloadStrategy(ABC):
    @abstractmethod
    def download(self, url, destination_path):
        """
        Download a file from the given URL to the destination path.
        
        Args:
            url: The URL to download from
            destination_path: The path where the file should be saved
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def pause(self):
        """
        Pause the current download.
        
        Returns:
            bool: True if paused successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def resume(self):
        """
        Resume a paused download.
        
        Returns:
            bool: True if resumed successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def cancel(self):
        """
        Cancel the current download.
        
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_progress(self):
        """
        Get the current download progress.
        
        Returns:
            float: Download progress as a percentage (0-100)
        """
        pass

import os
import requests
import threading
import concurrent.futures
from ..interfaces.IDownloadStrategy import IDownloadStrategy

class ParallelDownloadStrategy(IDownloadStrategy):
    def __init__(self, num_chunks=4):
        """
        Initialize the parallel download strategy.
        
        Args:
            num_chunks: Number of chunks to split the download into
        """
        self.url = None
        self.destination_path = None
        self.num_chunks = num_chunks
        self.is_paused = False
        self.is_cancelled = False
        self.progress = 0.0
        self.downloaded_size = 0
        self.file_size = 0
        self.download_thread = None
        self.chunk_threads = []
        self.callback = None
        self.lock = threading.Lock()  # For thread-safe operations
    
    def download(self, url, destination_path, callback=None):
        """
        Download a file from the given URL to the destination path using parallel chunks.
        
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
        self.downloaded_size = 0
        self.progress = 0.0
        
        # Start download in a separate thread
        self.download_thread = threading.Thread(target=self._download_thread)
        self.download_thread.daemon = True
        self.download_thread.start()
        
        return True
    
    def _download_thread(self):
        """Internal method to handle the parallel download process."""
        try:
            # Make a HEAD request to get file size
            response = requests.head(self.url, allow_redirects=True)
            self.file_size = int(response.headers.get('content-length', 0))
            
            if self.file_size <= 0:
                # If file size is unknown or zero, fall back to simple download
                self._simple_download()
                return
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
            
            # Create empty file of required size
            with open(self.destination_path, 'wb') as f:
                f.seek(self.file_size - 1)
                f.write(b'\0')
            
            # Calculate chunk sizes
            chunk_size = self.file_size // self.num_chunks
            chunks = []
            
            for i in range(self.num_chunks):
                start = i * chunk_size
                end = self.file_size - 1 if i == self.num_chunks - 1 else (i + 1) * chunk_size - 1
                chunks.append((start, end))
            
            # Download chunks in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_chunks) as executor:
                futures = [executor.submit(self._download_chunk, i, start, end) 
                          for i, (start, end) in enumerate(chunks)]
                
                # Wait for all chunks to complete
                for future in concurrent.futures.as_completed(futures):
                    if self.is_cancelled:
                        executor.shutdown(wait=False)
                        break
            
            # If download was cancelled, delete the partial file
            if self.is_cancelled:
                if os.path.exists(self.destination_path):
                    os.remove(self.destination_path)
                return
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.file_size, self.file_size)
        
        except Exception as e:
            # Handle download errors
            if self.callback:
                self.callback(error=str(e))
    
    def _download_chunk(self, chunk_id, start, end):
        """
        Download a specific chunk of the file.
        
        Args:
            chunk_id: ID of the chunk
            start: Start byte position
            end: End byte position
        """
        headers = {'Range': f'bytes={start}-{end}'}
        
        try:
            response = requests.get(self.url, headers=headers, stream=True)
            response.raise_for_status()
            
            with open(self.destination_path, 'r+b') as f:
                f.seek(start)
                
                for data in response.iter_content(chunk_size=8192):
                    if self.is_cancelled:
                        return
                    
                    if self.is_paused:
                        # Wait while paused
                        while self.is_paused and not self.is_cancelled:
                            threading.Event().wait(0.1)
                        if self.is_cancelled:
                            return
                    
                    if data:
                        f.write(data)
                        with self.lock:
                            self.downloaded_size += len(data)
                            self.progress = (self.downloaded_size / self.file_size * 100)
                            
                            # Call progress callback if provided
                            if self.callback:
                                self.callback(self.downloaded_size, self.file_size)
        
        except Exception as e:
            # Handle chunk download errors
            if self.callback:
                self.callback(error=f"Chunk {chunk_id} error: {str(e)}")
    
    def _simple_download(self):
        """Fall back to simple download if parallel download is not possible."""
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                
                with open(self.destination_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.is_cancelled:
                            f.close()
                            if os.path.exists(self.destination_path):
                                os.remove(self.destination_path)
                            return
                        
                        if self.is_paused:
                            while self.is_paused and not self.is_cancelled:
                                threading.Event().wait(0.1)
                            if self.is_cancelled:
                                continue
                        
                        if chunk:
                            f.write(chunk)
                            self.downloaded_size += len(chunk)
                            
                            # Call progress callback if provided
                            if self.callback:
                                self.callback(self.downloaded_size, self.file_size)
            
            # Set progress to 100% when complete
            if not self.is_cancelled:
                self.progress = 100.0
                if self.callback:
                    self.callback(self.file_size, self.file_size)
        
        except Exception as e:
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

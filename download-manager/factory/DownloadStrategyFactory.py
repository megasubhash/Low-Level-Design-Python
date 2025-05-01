from ..enums.DownloadType import DownloadType
from ..strategies.SimpleDownloadStrategy import SimpleDownloadStrategy
from ..strategies.ParallelDownloadStrategy import ParallelDownloadStrategy
from ..strategies.ResumeDownloadStrategy import ResumeDownloadStrategy

class DownloadStrategyFactory:
    @staticmethod
    def create_strategy(download_type=DownloadType.SIMPLE, **kwargs):
        """
        Create a download strategy based on the specified type.
        
        Args:
            download_type: The type of download strategy to create
            **kwargs: Additional parameters for specific strategies
            
        Returns:
            IDownloadStrategy: An instance of the requested download strategy
        """
        if download_type == DownloadType.SIMPLE:
            return SimpleDownloadStrategy()
        elif download_type == DownloadType.PARALLEL:
            num_chunks = kwargs.get('num_chunks', 4)
            return ParallelDownloadStrategy(num_chunks=num_chunks)
        elif download_type == DownloadType.RESUMABLE:
            return ResumeDownloadStrategy()
        else:
            # Default to simple download strategy
            return SimpleDownloadStrategy()

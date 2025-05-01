from abc import ABC, abstractmethod

class ISchedulingStrategy(ABC):
    """Interface for job scheduling strategies."""
    
    @abstractmethod
    def get_next_job(self, job_queue):
        """
        Get the next job to execute from the queue.
        
        Args:
            job_queue: Queue of jobs
            
        Returns:
            Job: The next job to execute, or None if no jobs are available
        """
        pass

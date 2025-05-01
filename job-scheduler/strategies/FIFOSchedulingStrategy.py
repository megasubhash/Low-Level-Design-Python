from interfaces.ISchedulingStrategy import ISchedulingStrategy

class FIFOSchedulingStrategy(ISchedulingStrategy):
    """
    First In, First Out scheduling strategy.
    
    Jobs are executed in the order they were added to the queue.
    """
    
    def get_next_job(self, job_queue):
        """
        Get the next job to execute from the queue using FIFO scheduling.
        
        Args:
            job_queue: Queue of jobs
            
        Returns:
            Job: The next job to execute, or None if no jobs are available
        """
        return job_queue.get_next_job_fifo()

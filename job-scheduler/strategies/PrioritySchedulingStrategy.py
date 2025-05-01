from interfaces.ISchedulingStrategy import ISchedulingStrategy

class PrioritySchedulingStrategy(ISchedulingStrategy):
    """
    Priority-based scheduling strategy.
    
    Jobs with higher priority are executed first.
    """
    
    def get_next_job(self, job_queue):
        """
        Get the next job to execute from the queue using priority-based scheduling.
        
        Args:
            job_queue: Queue of jobs
            
        Returns:
            Job: The next job to execute, or None if no jobs are available
        """
        return job_queue.get_next_job_priority()

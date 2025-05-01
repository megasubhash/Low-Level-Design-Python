from interfaces.ISchedulingStrategy import ISchedulingStrategy
from enums.JobStatus import JobStatus

class RoundRobinSchedulingStrategy(ISchedulingStrategy):
    """
    Round-robin scheduling strategy.
    
    Jobs are executed in a circular order, giving each job a fair share of CPU time.
    """
    
    def __init__(self, time_slice=1):
        """
        Initialize a RoundRobinSchedulingStrategy.
        
        Args:
            time_slice (int): Time slice for each job in seconds
        """
        self.time_slice = time_slice
        self.current_index = 0
    
    def get_next_job(self, job_queue):
        """
        Get the next job to execute from the queue using round-robin scheduling.
        
        Args:
            job_queue: Queue of jobs
            
        Returns:
            Job: The next job to execute, or None if no jobs are available
        """
        pending_jobs = job_queue.get_jobs_by_status(JobStatus.PENDING)
        
        if not pending_jobs:
            return None
        
        # Reset index if it's out of bounds
        if self.current_index >= len(pending_jobs):
            self.current_index = 0
        
        # Find the next ready job
        start_index = self.current_index
        while True:
            job = pending_jobs[self.current_index]
            
            # Move to the next job for the next call
            self.current_index = (self.current_index + 1) % len(pending_jobs)
            
            # Check if job is ready to run
            if not job.has_dependencies() or job.is_ready(job_queue.completed_jobs):
                return job
            
            # If we've checked all jobs and none are ready, return None
            if self.current_index == start_index:
                return None

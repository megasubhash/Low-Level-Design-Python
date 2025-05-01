import uuid
from datetime import datetime
from enums.JobStatus import JobStatus
from enums.JobPriority import JobPriority

class Job:
    """Represents a job in the scheduler system."""
    
    def __init__(self, job_id=None, name=None, function=None, args=None, kwargs=None,
                 priority=None, scheduled_time=None, deadline=None,
                 max_retries=0, retry_delay=0):
        """
        Initialize a Job object.
        
        Args:
            job_id (str, optional): Unique identifier for the job
            name (str, optional): Name of the job
            function (callable): Function to execute
            args (tuple, optional): Positional arguments for the function
            kwargs (dict, optional): Keyword arguments for the function
            priority (JobPriority): Priority of the job
            scheduled_time (datetime, optional): When the job should be executed
            deadline (datetime, optional): Deadline for job completion
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay in seconds between retries
        """
        self.id = job_id or str(uuid.uuid4())
        self.name = name or f"Job-{self.id[:8]}"
        self.function = function
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.priority = priority if priority is not None else JobPriority.MEDIUM
        self.status = JobStatus.PENDING
        self.created_at = datetime.now()
        self.scheduled_time = scheduled_time
        self.deadline = deadline
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_count = 0
        self.dependencies = set()  # Set of job IDs that must complete before this job
        
    def __str__(self):
        return (f"Job(id={self.id}, name={self.name}, status={self.status.value}, "
                f"priority={self.priority.value})")
    
    def add_dependency(self, job_id):
        """
        Add a dependency for this job.
        
        Args:
            job_id (str): ID of the job that must complete before this job
        """
        self.dependencies.add(job_id)
    
    def remove_dependency(self, job_id):
        """
        Remove a dependency for this job.
        
        Args:
            job_id (str): ID of the job to remove as a dependency
        """
        if job_id in self.dependencies:
            self.dependencies.remove(job_id)
    
    def has_dependencies(self):
        """
        Check if the job has any dependencies.
        
        Returns:
            bool: True if the job has dependencies, False otherwise
        """
        return len(self.dependencies) > 0
    
    def is_ready(self, completed_jobs):
        """
        Check if the job is ready to run (all dependencies completed).
        
        Args:
            completed_jobs (set): Set of completed job IDs
            
        Returns:
            bool: True if the job is ready to run, False otherwise
        """
        return all(dep_id in completed_jobs for dep_id in self.dependencies)
    
    def is_scheduled(self):
        """
        Check if the job is scheduled for future execution.
        
        Returns:
            bool: True if the job is scheduled, False otherwise
        """
        if not self.scheduled_time:
            return False
        return self.scheduled_time > datetime.now()
    
    def is_expired(self):
        """
        Check if the job has exceeded its deadline.
        
        Returns:
            bool: True if the job is expired, False otherwise
        """
        if not self.deadline:
            return False
        return datetime.now() > self.deadline
    
    def mark_running(self):
        """Mark the job as running."""
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now()
    
    def mark_completed(self, result=None):
        """
        Mark the job as completed.
        
        Args:
            result: Result of the job execution
        """
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
    
    def mark_failed(self, error=None):
        """
        Mark the job as failed.
        
        Args:
            error: Error that caused the job to fail
        """
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
    
    def mark_cancelled(self):
        """Mark the job as cancelled."""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now()
    
    def should_retry(self):
        """
        Check if the job should be retried.
        
        Returns:
            bool: True if the job should be retried, False otherwise
        """
        return (self.status == JobStatus.FAILED and 
                self.retry_count < self.max_retries)
    
    def increment_retry(self):
        """
        Increment the retry count and reset the job status.
        
        Returns:
            bool: True if the job was reset for retry, False otherwise
        """
        if self.retry_count >= self.max_retries:
            return False
        
        self.retry_count += 1
        self.status = JobStatus.PENDING
        return True
    
    def execute(self):
        """
        Execute the job function.
        
        Returns:
            The result of the function execution
        
        Raises:
            Exception: If the function execution fails
        """
        try:
            self.mark_running()
            result = self.function(*self.args, **self.kwargs)
            self.mark_completed(result)
            return result
        except Exception as e:
            self.mark_failed(str(e))
            raise

import threading
import time
from datetime import datetime, timedelta
from models.Job import Job
from models.JobQueue import JobQueue
from enums.JobStatus import JobStatus
from enums.SchedulingStrategy import SchedulingStrategy
from factory.SchedulingStrategyFactory import SchedulingStrategyFactory

class JobSchedulerService:
    """Service for scheduling and executing jobs."""
    
    def __init__(self, strategy_type=SchedulingStrategy.PRIORITY, max_workers=5, poll_interval=1):
        """
        Initialize a JobSchedulerService.
        
        Args:
            strategy_type (SchedulingStrategy): Type of scheduling strategy to use
            max_workers (int): Maximum number of concurrent worker threads
            poll_interval (int): Interval in seconds to poll for scheduled jobs
        """
        self.job_queue = JobQueue()
        self.strategy = SchedulingStrategyFactory.create_strategy(strategy_type)
        self.max_workers = max_workers
        self.poll_interval = poll_interval
        self.running = False
        self.workers = []
        self.scheduler_thread = None
        self.lock = threading.Lock()
    
    def schedule_job(self, function, args=None, kwargs=None, name=None, priority=None,
                    scheduled_time=None, deadline=None, max_retries=0, retry_delay=0):
        """
        Schedule a job for execution.
        
        Args:
            function (callable): Function to execute
            args (tuple, optional): Positional arguments for the function
            kwargs (dict, optional): Keyword arguments for the function
            name (str, optional): Name of the job
            priority (JobPriority, optional): Priority of the job
            scheduled_time (datetime, optional): When the job should be executed
            deadline (datetime, optional): Deadline for job completion
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay in seconds between retries
            
        Returns:
            str: ID of the scheduled job
        """
        job = Job(
            name=name,
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority,
            scheduled_time=scheduled_time,
            deadline=deadline,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        with self.lock:
            self.job_queue.add_job(job)
        
        return job.id
    
    def schedule_job_after_delay(self, delay_seconds, function, args=None, kwargs=None,
                               name=None, priority=None, deadline=None, max_retries=0, retry_delay=0):
        """
        Schedule a job for execution after a delay.
        
        Args:
            delay_seconds (int): Delay in seconds before executing the job
            function (callable): Function to execute
            args (tuple, optional): Positional arguments for the function
            kwargs (dict, optional): Keyword arguments for the function
            name (str, optional): Name of the job
            priority (JobPriority, optional): Priority of the job
            deadline (datetime, optional): Deadline for job completion
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay in seconds between retries
            
        Returns:
            str: ID of the scheduled job
        """
        scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
        
        return self.schedule_job(
            function=function,
            args=args,
            kwargs=kwargs,
            name=name,
            priority=priority,
            scheduled_time=scheduled_time,
            deadline=deadline,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
    
    def add_job_dependency(self, job_id, dependency_job_id):
        """
        Add a dependency to a job.
        
        Args:
            job_id (str): ID of the job
            dependency_job_id (str): ID of the job that must complete before job_id
            
        Returns:
            bool: True if dependency was added, False otherwise
        """
        with self.lock:
            job = self.job_queue.get_job(job_id)
            if not job:
                return False
            
            dependency_job = self.job_queue.get_job(dependency_job_id)
            if not dependency_job:
                return False
            
            job.add_dependency(dependency_job_id)
            return True
    
    def cancel_job(self, job_id):
        """
        Cancel a job.
        
        Args:
            job_id (str): ID of the job to cancel
            
        Returns:
            bool: True if job was cancelled, False otherwise
        """
        with self.lock:
            job = self.job_queue.get_job(job_id)
            if not job or job.status not in [JobStatus.PENDING, JobStatus.SCHEDULED]:
                return False
            
            job.mark_cancelled()
            return True
    
    def get_job(self, job_id):
        """
        Get a job by ID.
        
        Args:
            job_id (str): ID of the job
            
        Returns:
            Job: The job, or None if not found
        """
        with self.lock:
            return self.job_queue.get_job(job_id)
    
    def get_all_jobs(self):
        """
        Get all jobs.
        
        Returns:
            list: List of all jobs
        """
        with self.lock:
            return self.job_queue.get_all_jobs()
    
    def get_jobs_by_status(self, status):
        """
        Get jobs by status.
        
        Args:
            status (JobStatus): Status to filter by
            
        Returns:
            list: List of jobs with the specified status
        """
        with self.lock:
            return self.job_queue.get_jobs_by_status(status)
    
    def start(self):
        """Start the job scheduler."""
        if self.running:
            return
        
        self.running = True
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        # Start worker threads
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def stop(self):
        """Stop the job scheduler."""
        self.running = False
        
        # Wait for threads to terminate
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        
        for worker in self.workers:
            worker.join(timeout=2)
        
        self.workers = []
        self.scheduler_thread = None
    
    def _scheduler_loop(self):
        """Main loop for the scheduler thread."""
        while self.running:
            try:
                with self.lock:
                    # Check for scheduled jobs that are ready to run
                    self.job_queue.get_scheduled_jobs()
                
                # Sleep for poll interval
                time.sleep(self.poll_interval)
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
    
    def _worker_loop(self):
        """Main loop for worker threads."""
        while self.running:
            job = None
            
            try:
                # Get the next job to execute
                with self.lock:
                    job = self.strategy.get_next_job(self.job_queue)
                
                if job:
                    # Execute the job
                    self._execute_job(job)
                else:
                    # No jobs available, sleep for a short time
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error in worker loop: {e}")
                
                # If job failed, mark it as failed
                if job:
                    with self.lock:
                        job.mark_failed(str(e))
    
    def _execute_job(self, job):
        """
        Execute a job.
        
        Args:
            job: Job to execute
        """
        try:
            # Execute the job
            result = job.execute()
            
            # Mark job as completed
            with self.lock:
                self.job_queue.mark_job_completed(job.id)
            
            return result
        except Exception as e:
            # Check if job should be retried
            if job.should_retry():
                # Schedule retry after delay
                if job.retry_delay > 0:
                    time.sleep(job.retry_delay)
                
                with self.lock:
                    job.increment_retry()
            else:
                # Mark job as failed
                with self.lock:
                    job.mark_failed(str(e))
            
            return None

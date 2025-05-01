import heapq
from datetime import datetime
from enums.JobStatus import JobStatus
from enums.JobPriority import JobPriority

class JobQueue:
    """Represents a queue of jobs in the scheduler system."""
    
    def __init__(self):
        """Initialize a JobQueue object."""
        self.jobs = {}  # Map of job_id to Job
        self.priority_queue = []  # Heap for priority-based scheduling
        self.fifo_queue = []  # List for FIFO scheduling
        self.deadline_queue = []  # Heap for deadline-based scheduling
        self.scheduled_queue = []  # Heap for scheduled jobs
        self.completed_jobs = set()  # Set of completed job IDs
    
    def add_job(self, job):
        """
        Add a job to the queue.
        
        Args:
            job: Job to add
            
        Returns:
            bool: True if job was added, False otherwise
        """
        if job.id in self.jobs:
            return False
        
        self.jobs[job.id] = job
        
        # If job is scheduled for future execution
        if job.scheduled_time and job.scheduled_time > datetime.now():
            job.status = JobStatus.SCHEDULED
            heapq.heappush(self.scheduled_queue, (job.scheduled_time, job.id))
            return True
        
        # Add to appropriate queue based on job properties
        if job.deadline:
            heapq.heappush(self.deadline_queue, (job.deadline, job.id))
        
        heapq.heappush(self.priority_queue, (-job.priority.value, job.created_at, job.id))
        self.fifo_queue.append(job.id)
        
        return True
    
    def remove_job(self, job_id):
        """
        Remove a job from the queue.
        
        Args:
            job_id (str): ID of the job to remove
            
        Returns:
            Job: The removed job, or None if not found
        """
        if job_id not in self.jobs:
            return None
        
        job = self.jobs.pop(job_id)
        
        # Note: We don't remove from the internal queues for efficiency
        # The job will be skipped when it's popped from the queue
        
        return job
    
    def get_job(self, job_id):
        """
        Get a job by ID.
        
        Args:
            job_id (str): ID of the job
            
        Returns:
            Job: The job, or None if not found
        """
        return self.jobs.get(job_id)
    
    def mark_job_completed(self, job_id):
        """
        Mark a job as completed.
        
        Args:
            job_id (str): ID of the job
            
        Returns:
            bool: True if job was marked as completed, False otherwise
        """
        job = self.get_job(job_id)
        if not job:
            return False
        
        job.mark_completed()
        self.completed_jobs.add(job_id)
        return True
    
    def get_next_job_fifo(self):
        """
        Get the next job using FIFO scheduling.
        
        Returns:
            Job: The next job, or None if no jobs are available
        """
        while self.fifo_queue:
            job_id = self.fifo_queue[0]
            job = self.get_job(job_id)
            
            # Skip jobs that are no longer in the queue or not ready
            if not job or job.status != JobStatus.PENDING or job.has_dependencies() and not job.is_ready(self.completed_jobs):
                self.fifo_queue.pop(0)
                continue
            
            return job
        
        return None
    
    def get_next_job_priority(self):
        """
        Get the next job using priority-based scheduling.
        
        Returns:
            Job: The next job, or None if no jobs are available
        """
        while self.priority_queue:
            _, _, job_id = self.priority_queue[0]
            job = self.get_job(job_id)
            
            # Skip jobs that are no longer in the queue or not ready
            if not job or job.status != JobStatus.PENDING or job.has_dependencies() and not job.is_ready(self.completed_jobs):
                heapq.heappop(self.priority_queue)
                continue
            
            return job
        
        return None
    
    def get_next_job_deadline(self):
        """
        Get the next job using deadline-based scheduling.
        
        Returns:
            Job: The next job, or None if no jobs are available
        """
        while self.deadline_queue:
            _, job_id = self.deadline_queue[0]
            job = self.get_job(job_id)
            
            # Skip jobs that are no longer in the queue or not ready
            if not job or job.status != JobStatus.PENDING or job.has_dependencies() and not job.is_ready(self.completed_jobs):
                heapq.heappop(self.deadline_queue)
                continue
            
            return job
        
        return None
    
    def get_scheduled_jobs(self):
        """
        Get jobs that are scheduled to run now.
        
        Returns:
            list: List of jobs that are ready to run
        """
        now = datetime.now()
        ready_jobs = []
        
        while self.scheduled_queue and self.scheduled_queue[0][0] <= now:
            scheduled_time, job_id = heapq.heappop(self.scheduled_queue)
            job = self.get_job(job_id)
            
            if job and job.status == JobStatus.SCHEDULED:
                job.status = JobStatus.PENDING
                ready_jobs.append(job)
                
                # Add to appropriate queue
                if job.deadline:
                    heapq.heappush(self.deadline_queue, (job.deadline, job.id))
                
                heapq.heappush(self.priority_queue, (-job.priority.value, job.created_at, job.id))
                self.fifo_queue.append(job.id)
        
        return ready_jobs
    
    def get_all_jobs(self):
        """
        Get all jobs in the queue.
        
        Returns:
            list: List of all jobs
        """
        return list(self.jobs.values())
    
    def get_jobs_by_status(self, status):
        """
        Get jobs by status.
        
        Args:
            status (JobStatus): Status to filter by
            
        Returns:
            list: List of jobs with the specified status
        """
        return [job for job in self.jobs.values() if job.status == status]
    
    def clear(self):
        """Clear the queue."""
        self.jobs.clear()
        self.priority_queue.clear()
        self.fifo_queue.clear()
        self.deadline_queue.clear()
        self.scheduled_queue.clear()
        self.completed_jobs.clear()

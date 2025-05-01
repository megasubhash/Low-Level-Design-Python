import time
import random
from datetime import datetime, timedelta
from services.JobSchedulerService import JobSchedulerService
from enums.SchedulingStrategy import SchedulingStrategy
from enums.JobPriority import JobPriority
from enums.JobStatus import JobStatus

# Example job functions
def simple_job(job_name):
    """A simple job that prints its name."""
    print(f"Executing {job_name}")
    return f"{job_name} completed successfully"

def long_job(job_name, duration):
    """A job that takes some time to complete."""
    print(f"Starting {job_name} (duration: {duration}s)")
    time.sleep(duration)
    print(f"Completed {job_name}")
    return f"{job_name} completed after {duration}s"

def failing_job(job_name, fail_probability=0.7):
    """A job that might fail."""
    print(f"Executing {job_name} (fail probability: {fail_probability})")
    if random.random() < fail_probability:
        raise Exception(f"{job_name} failed deliberately")
    return f"{job_name} completed successfully"

def print_job_info(job):
    """Print information about a job."""
    print(f"Job: {job.name} (ID: {job.id})")
    print(f"Status: {job.status.value}")
    print(f"Priority: {job.priority.value}")
    
    if job.scheduled_time:
        print(f"Scheduled Time: {job.scheduled_time}")
    
    if job.started_at:
        print(f"Started At: {job.started_at}")
    
    if job.completed_at:
        print(f"Completed At: {job.completed_at}")
    
    if job.result:
        print(f"Result: {job.result}")
    
    if job.error:
        print(f"Error: {job.error}")
    
    if job.retry_count > 0:
        print(f"Retry Count: {job.retry_count}/{job.max_retries}")
    
    if job.dependencies:
        print(f"Dependencies: {job.dependencies}")
    
    print("-" * 50)

def demo_fifo_scheduling():
    """Demonstrate FIFO scheduling."""
    print("\n=== FIFO Scheduling Demo ===")
    
    # Create scheduler with FIFO strategy
    scheduler = JobSchedulerService(strategy_type=SchedulingStrategy.FIFO, max_workers=2)
    scheduler.start()
    
    # Schedule some jobs
    job1_id = scheduler.schedule_job(
        function=simple_job,
        args=("FIFO Job 1",),
        name="FIFO Job 1"
    )
    
    job2_id = scheduler.schedule_job(
        function=simple_job,
        args=("FIFO Job 2",),
        name="FIFO Job 2"
    )
    
    job3_id = scheduler.schedule_job(
        function=simple_job,
        args=("FIFO Job 3",),
        name="FIFO Job 3"
    )
    
    # Wait for jobs to complete
    time.sleep(3)
    
    # Get and print job info
    print("\nJob Results:")
    for job_id in [job1_id, job2_id, job3_id]:
        job = scheduler.get_job(job_id)
        print_job_info(job)
    
    # Stop the scheduler
    scheduler.stop()
    
    return scheduler

def demo_priority_scheduling():
    """Demonstrate priority-based scheduling."""
    print("\n=== Priority Scheduling Demo ===")
    
    # Create scheduler with priority strategy
    scheduler = JobSchedulerService(strategy_type=SchedulingStrategy.PRIORITY, max_workers=1)
    scheduler.start()
    
    # Schedule jobs with different priorities
    job1_id = scheduler.schedule_job(
        function=long_job,
        args=("Low Priority Job", 1),
        name="Low Priority Job",
        priority=JobPriority.LOW
    )
    
    job2_id = scheduler.schedule_job(
        function=long_job,
        args=("Medium Priority Job", 1),
        name="Medium Priority Job",
        priority=JobPriority.MEDIUM
    )
    
    job3_id = scheduler.schedule_job(
        function=long_job,
        args=("High Priority Job", 1),
        name="High Priority Job",
        priority=JobPriority.HIGH
    )
    
    job4_id = scheduler.schedule_job(
        function=long_job,
        args=("Critical Priority Job", 1),
        name="Critical Priority Job",
        priority=JobPriority.CRITICAL
    )
    
    # Wait for jobs to complete
    time.sleep(5)
    
    # Get and print job info
    print("\nJob Results (should execute in order of priority):")
    for job_id in [job1_id, job2_id, job3_id, job4_id]:
        job = scheduler.get_job(job_id)
        print_job_info(job)
    
    # Stop the scheduler
    scheduler.stop()
    
    return scheduler

def demo_scheduled_jobs():
    """Demonstrate scheduled jobs."""
    print("\n=== Scheduled Jobs Demo ===")
    
    # Create scheduler
    scheduler = JobSchedulerService(max_workers=2)
    scheduler.start()
    
    # Get current time
    now = datetime.now()
    
    # Schedule jobs for future execution
    job1_id = scheduler.schedule_job(
        function=simple_job,
        args=("Immediate Job",),
        name="Immediate Job"
    )
    
    job2_id = scheduler.schedule_job(
        function=simple_job,
        args=("Scheduled Job (2s)",),
        name="Scheduled Job (2s)",
        scheduled_time=now + timedelta(seconds=2)
    )
    
    job3_id = scheduler.schedule_job(
        function=simple_job,
        args=("Scheduled Job (4s)",),
        name="Scheduled Job (4s)",
        scheduled_time=now + timedelta(seconds=4)
    )
    
    # Alternative way to schedule delayed jobs
    job4_id = scheduler.schedule_job_after_delay(
        delay_seconds=6,
        function=simple_job,
        args=("Delayed Job (6s)",),
        name="Delayed Job (6s)"
    )
    
    # Print initial job statuses
    print("\nInitial Job Statuses:")
    for job_id in [job1_id, job2_id, job3_id, job4_id]:
        job = scheduler.get_job(job_id)
        print(f"Job: {job.name}, Status: {job.status.value}")
    
    # Wait for all jobs to complete
    time.sleep(8)
    
    # Get and print job info
    print("\nJob Results:")
    for job_id in [job1_id, job2_id, job3_id, job4_id]:
        job = scheduler.get_job(job_id)
        print_job_info(job)
    
    # Stop the scheduler
    scheduler.stop()
    
    return scheduler

def demo_job_dependencies():
    """Demonstrate job dependencies."""
    print("\n=== Job Dependencies Demo ===")
    
    # Create scheduler
    scheduler = JobSchedulerService(max_workers=1)
    scheduler.start()
    
    # Schedule jobs with dependencies
    job1_id = scheduler.schedule_job(
        function=long_job,
        args=("Parent Job", 1),
        name="Parent Job"
    )
    
    job2_id = scheduler.schedule_job(
        function=simple_job,
        args=("Child Job 1",),
        name="Child Job 1"
    )
    
    job3_id = scheduler.schedule_job(
        function=simple_job,
        args=("Child Job 2",),
        name="Child Job 2"
    )
    
    # Add dependencies
    scheduler.add_job_dependency(job2_id, job1_id)  # job2 depends on job1
    scheduler.add_job_dependency(job3_id, job2_id)  # job3 depends on job2
    
    # Wait for jobs to complete
    time.sleep(5)
    
    # Get and print job info
    print("\nJob Results (should execute in dependency order):")
    for job_id in [job1_id, job2_id, job3_id]:
        job = scheduler.get_job(job_id)
        print_job_info(job)
    
    # Stop the scheduler
    scheduler.stop()
    
    return scheduler

def demo_job_retries():
    """Demonstrate job retries."""
    print("\n=== Job Retries Demo ===")
    
    # Create scheduler
    scheduler = JobSchedulerService(max_workers=1)
    scheduler.start()
    
    # Schedule a job that will fail with retries
    job_id = scheduler.schedule_job(
        function=failing_job,
        args=("Failing Job", 0.8),
        name="Failing Job",
        max_retries=3,
        retry_delay=1
    )
    
    # Wait for job to complete or exhaust retries
    time.sleep(8)
    
    # Get and print job info
    print("\nJob Result:")
    job = scheduler.get_job(job_id)
    print_job_info(job)
    
    # Stop the scheduler
    scheduler.stop()
    
    return scheduler

def main():
    print("Job Scheduler System Demo")
    print("=========================\n")
    
    # Run demos
    demo_fifo_scheduling()
    demo_priority_scheduling()
    demo_scheduled_jobs()
    demo_job_dependencies()
    demo_job_retries()

if __name__ == "__main__":
    main()

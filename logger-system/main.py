import time
import threading
import random
import os
from typing import List

from log_level import LogLevel
from logger_factory import LoggerFactory
from filters import RegexFilter, RateLimitFilter


def setup_logger_from_config():
    """Set up loggers from configuration file."""
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Configure loggers from file
    LoggerFactory.configure_from_file("config.json")
    
    return LoggerFactory.get_logger("app")


def setup_logger_programmatically():
    """Set up loggers programmatically."""
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Get the root logger
    root_logger = LoggerFactory.get_logger("root")
    root_logger.set_level(LogLevel.WARNING)
    root_logger.add_console_handler(LogLevel.WARNING)
    
    # Create an application logger
    app_logger = LoggerFactory.get_logger("app")
    app_logger.set_level(LogLevel.DEBUG)
    app_logger.propagate = False
    
    # Add console handler
    app_logger.add_console_handler(LogLevel.INFO)
    
    # Add file handler
    app_logger.add_file_handler("logs/app.log", LogLevel.DEBUG)
    
    # Add rotating file handler for errors
    app_logger.add_rotating_file_handler(
        "logs/errors.log", 
        LogLevel.ERROR,
        max_bytes=5 * 1024 * 1024,  # 5 MB
        backup_count=10
    )
    
    # Add a filter to exclude certain messages
    app_logger.add_filter(RegexFilter(r"spam", include=False))
    
    # Add a rate limit filter to prevent log flooding
    app_logger.add_filter(RateLimitFilter(max_records=100, time_window=1.0))
    
    return app_logger


def worker(logger, worker_id: int, iterations: int):
    """Worker function that generates log messages."""
    logger.info(f"Worker {worker_id} started", worker_id=worker_id)
    
    for i in range(iterations):
        # Simulate some work
        time.sleep(random.uniform(0.1, 0.5))
        
        # Log with different levels based on random chance
        r = random.random()
        
        if r < 0.6:
            logger.debug(f"Worker {worker_id} iteration {i}: debug message", 
                         worker_id=worker_id, iteration=i)
        elif r < 0.8:
            logger.info(f"Worker {worker_id} iteration {i}: info message", 
                        worker_id=worker_id, iteration=i)
        elif r < 0.9:
            logger.warning(f"Worker {worker_id} iteration {i}: warning message", 
                           worker_id=worker_id, iteration=i)
        elif r < 0.95:
            logger.error(f"Worker {worker_id} iteration {i}: error message", 
                         worker_id=worker_id, iteration=i)
        else:
            try:
                # Simulate an exception
                result = 1 / 0
            except Exception as e:
                logger.exception(f"Worker {worker_id} iteration {i}: exception occurred", 
                                 worker_id=worker_id, iteration=i)
    
    logger.info(f"Worker {worker_id} finished", worker_id=worker_id)


def demo_basic_logging(logger):
    """Demonstrate basic logging functionality."""
    print("\n=== Basic Logging Demo ===")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    try:
        # Simulate an exception
        result = 1 / 0
    except Exception as e:
        logger.exception("An exception occurred")


def demo_context_logging(logger):
    """Demonstrate context-based logging."""
    print("\n=== Context Logging Demo ===")
    
    # Log with context
    logger.info("Processing request", request_id="12345", user="admin")
    
    # Using context manager
    with logger.context(request_id="67890", user="guest"):
        logger.info("Request received")
        logger.debug("Processing request details")
        
        # Nested context
        with logger.context(subsystem="auth"):
            logger.info("Authenticating user")
            logger.debug("Checking credentials")
        
        logger.info("Request processed")


def demo_threaded_logging(logger):
    """Demonstrate logging from multiple threads."""
    print("\n=== Threaded Logging Demo ===")
    
    # Create and start worker threads
    threads: List[threading.Thread] = []
    num_workers = 3
    iterations = 5
    
    for i in range(num_workers):
        thread = threading.Thread(target=worker, args=(logger, i, iterations))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()


def main():
    """Main function to demonstrate the logger system."""
    print("=== Logger System Demo ===")
    
    # Choose configuration method
    use_config_file = True
    
    if use_config_file:
        logger = setup_logger_from_config()
        print("Loggers configured from config.json")
    else:
        logger = setup_logger_programmatically()
        print("Loggers configured programmatically")
    
    # Get specialized loggers
    api_logger = LoggerFactory.get_logger("app.api")
    db_logger = LoggerFactory.get_logger("app.db")
    
    # Run demos
    demo_basic_logging(logger)
    demo_context_logging(logger)
    
    # Log some messages with specialized loggers
    api_logger.info("API server started")
    api_logger.debug("Registered endpoints: /users, /products, /orders")
    
    db_logger.info("Database connection established")
    db_logger.debug("Using connection pool with 10 connections")
    
    # Demonstrate threaded logging
    demo_threaded_logging(logger)
    
    # Shutdown loggers
    print("\nShutting down loggers...")
    LoggerFactory.shutdown()
    print("Done!")


if __name__ == "__main__":
    main()

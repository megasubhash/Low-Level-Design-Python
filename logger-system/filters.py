from typing import Callable, List, Dict, Any, Optional, Pattern
import re
from log_record import LogRecord


class Filter:
    """
    Base class for log filters.
    
    Filters determine whether a log record should be processed by a handler.
    """
    
    def __call__(self, record: LogRecord) -> bool:
        """
        Determine if a record should be processed.
        
        Args:
            record: The log record to check
            
        Returns:
            True if the record should be processed, False otherwise
        """
        return self.filter(record)
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        return True


class LoggerNameFilter(Filter):
    """Filter that only allows records from specific loggers."""
    
    def __init__(self, logger_names: List[str], include: bool = True):
        """
        Initialize the logger name filter.
        
        Args:
            logger_names: List of logger names to filter on
            include: If True, only records from the specified loggers will be included.
                    If False, records from the specified loggers will be excluded.
        """
        self.logger_names = logger_names
        self.include = include
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record based on its logger name.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        is_match = any(record.logger_name.startswith(name) for name in self.logger_names)
        return is_match if self.include else not is_match


class RegexFilter(Filter):
    """Filter that only allows records with messages matching a regular expression."""
    
    def __init__(self, pattern: str, include: bool = True):
        """
        Initialize the regex filter.
        
        Args:
            pattern: Regular expression pattern to match against log messages
            include: If True, only records with messages matching the pattern will be included.
                    If False, records with messages matching the pattern will be excluded.
        """
        self.pattern = re.compile(pattern)
        self.include = include
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record based on its message content.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        is_match = bool(self.pattern.search(record.message))
        return is_match if self.include else not is_match


class ContextFilter(Filter):
    """Filter that only allows records with specific context values."""
    
    def __init__(self, context_key: str, context_values: List[Any] = None, include: bool = True):
        """
        Initialize the context filter.
        
        Args:
            context_key: The context key to check
            context_values: List of values to match against the context key.
                          If None, just checks for the existence of the key.
            include: If True, only records with matching context will be included.
                    If False, records with matching context will be excluded.
        """
        self.context_key = context_key
        self.context_values = context_values
        self.include = include
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record based on its context.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        # Check if the context key exists
        if self.context_key not in record.context:
            return not self.include
        
        # If no specific values to check, just check for key existence
        if self.context_values is None:
            return self.include
        
        # Check if the context value matches any of the specified values
        is_match = record.context[self.context_key] in self.context_values
        return is_match if self.include else not is_match


class CompositeFilter(Filter):
    """A filter that combines multiple filters with AND or OR logic."""
    
    def __init__(self, filters: List[Filter], require_all: bool = True):
        """
        Initialize the composite filter.
        
        Args:
            filters: List of filters to combine
            require_all: If True, all filters must pass (AND logic).
                        If False, at least one filter must pass (OR logic).
        """
        self.filters = filters
        self.require_all = require_all
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record using multiple filters.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        if not self.filters:
            return True
        
        if self.require_all:
            # AND logic - all filters must pass
            return all(f.filter(record) for f in self.filters)
        else:
            # OR logic - at least one filter must pass
            return any(f.filter(record) for f in self.filters)


class RateLimitFilter(Filter):
    """Filter that limits the rate of log records."""
    
    def __init__(self, max_records: int, time_window: float):
        """
        Initialize the rate limit filter.
        
        Args:
            max_records: Maximum number of records to allow in the time window
            time_window: Time window in seconds
        """
        self.max_records = max_records
        self.time_window = time_window
        self.record_times = []
        import time
        self.time_func = time.time
    
    def filter(self, record: LogRecord) -> bool:
        """
        Filter a log record based on rate limiting.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be processed, False otherwise
        """
        current_time = self.time_func()
        
        # Remove old records outside the time window
        self.record_times = [t for t in self.record_times if current_time - t <= self.time_window]
        
        # Check if we've exceeded the maximum number of records
        if len(self.record_times) >= self.max_records:
            return False
        
        # Add the current record time
        self.record_times.append(current_time)
        return True

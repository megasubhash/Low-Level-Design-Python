import sys
import traceback
import threading
from typing import Dict, List, Optional, Any, Callable, Union

from log_level import LogLevel
from log_record import LogRecord
from handlers import Handler, ConsoleHandler, FileHandler, RotatingFileHandler, NetworkHandler, AsyncHandler
from formatters import Formatter, SimpleFormatter, DetailedFormatter, JsonFormatter
from filters import Filter


class Logger:
    """
    Main class for logging messages.
    
    This class provides methods for logging messages at different severity levels
    and manages a collection of handlers for outputting log records.
    """
    
    def __init__(self, name: str, level: LogLevel = LogLevel.DEBUG):
        """
        Initialize a new logger.
        
        Args:
            name: The name of the logger (typically the module name)
            level: The minimum log level this logger will process
        """
        self.name = name
        self.level = level
        self.handlers: List[Handler] = []
        self.filters: List[Filter] = []
        self.parent: Optional['Logger'] = None
        self.propagate: bool = True
        self._context_stack: List[Dict[str, Any]] = []
        self._context_lock = threading.RLock()
    
    def add_handler(self, handler: Handler) -> None:
        """
        Add a handler to this logger.
        
        Args:
            handler: The handler to add
        """
        self.handlers.append(handler)
    
    def remove_handler(self, handler: Handler) -> None:
        """
        Remove a handler from this logger.
        
        Args:
            handler: The handler to remove
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def add_filter(self, filter_obj: Filter) -> None:
        """
        Add a filter to this logger.
        
        Args:
            filter_obj: The filter to add
        """
        self.filters.append(filter_obj)
    
    def remove_filter(self, filter_obj: Filter) -> None:
        """
        Remove a filter from this logger.
        
        Args:
            filter_obj: The filter to remove
        """
        if filter_obj in self.filters:
            self.filters.remove(filter_obj)
    
    def set_level(self, level: LogLevel) -> None:
        """
        Set the minimum log level for this logger.
        
        Args:
            level: The new minimum log level
        """
        self.level = level
    
    def is_enabled_for(self, level: LogLevel) -> bool:
        """
        Check if this logger is enabled for the specified level.
        
        Args:
            level: The log level to check
            
        Returns:
            True if the logger is enabled for the level, False otherwise
        """
        return level.value >= self.level.value
    
    def _should_log(self, record: LogRecord) -> bool:
        """
        Determine if a record should be logged.
        
        Args:
            record: The log record to check
            
        Returns:
            True if the record should be logged, False otherwise
        """
        # Check if the record's level is high enough
        if not self.is_enabled_for(record.level):
            return False
        
        # Apply all filters
        for filter_obj in self.filters:
            if not filter_obj(record):
                return False
        
        return True
    
    def handle(self, record: LogRecord) -> None:
        """
        Handle a log record by passing it to all handlers.
        
        Args:
            record: The log record to handle
        """
        if not self._should_log(record):
            return
        
        # Add current context to the record
        if self._context_stack:
            with self._context_lock:
                for context_dict in self._context_stack:
                    record.add_context(**context_dict)
        
        # Pass the record to all handlers
        for handler in self.handlers:
            handler.handle(record)
        
        # Propagate to parent logger if enabled
        if self.propagate and self.parent:
            self.parent.handle(record)
    
    def log(self, level: LogLevel, msg: str, *args, **kwargs) -> None:
        """
        Log a message at the specified level.
        
        Args:
            level: The log level
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        if not self.is_enabled_for(level):
            return
        
        # Format the message if args are provided
        if args:
            msg = msg % args
        
        # Create a log record
        record = LogRecord(
            logger_name=self.name,
            level=level,
            message=msg
        )
        
        # Add any additional context
        if kwargs:
            record.add_context(**kwargs)
        
        # Handle the record
        self.handle(record)
    
    def debug(self, msg: str, *args, **kwargs) -> None:
        """
        Log a DEBUG level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        self.log(LogLevel.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs) -> None:
        """
        Log an INFO level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        self.log(LogLevel.INFO, msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs) -> None:
        """
        Log a WARNING level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        self.log(LogLevel.WARNING, msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs) -> None:
        """
        Log an ERROR level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        self.log(LogLevel.ERROR, msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs) -> None:
        """
        Log a CRITICAL level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            **kwargs: Additional context to include in the log record
        """
        self.log(LogLevel.CRITICAL, msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, exc_info=True, **kwargs) -> None:
        """
        Log an exception with an ERROR level message.
        
        Args:
            msg: The message to log
            *args: Arguments for string formatting
            exc_info: If True, include exception information in the log record
            **kwargs: Additional context to include in the log record
        """
        if exc_info:
            kwargs['exception_info'] = sys.exc_info()
        
        self.error(msg, *args, **kwargs)
    
    def add_console_handler(
        self, 
        level: LogLevel = LogLevel.INFO, 
        formatter: Optional[Formatter] = None,
        use_stderr_for_errors: bool = True
    ) -> ConsoleHandler:
        """
        Add a console handler to this logger.
        
        Args:
            level: The minimum log level for the handler
            formatter: The formatter to use
            use_stderr_for_errors: If True, use stderr for ERROR and CRITICAL messages
            
        Returns:
            The created handler
        """
        handler = ConsoleHandler(level, formatter, use_stderr_for_errors)
        self.add_handler(handler)
        return handler
    
    def add_file_handler(
        self, 
        filename: str, 
        level: LogLevel = LogLevel.DEBUG, 
        formatter: Optional[Formatter] = None,
        mode: str = 'a',
        encoding: str = 'utf-8'
    ) -> FileHandler:
        """
        Add a file handler to this logger.
        
        Args:
            filename: Path to the log file
            level: The minimum log level for the handler
            formatter: The formatter to use
            mode: File opening mode ('a' for append, 'w' for write)
            encoding: File encoding
            
        Returns:
            The created handler
        """
        handler = FileHandler(filename, level, formatter, mode, encoding)
        self.add_handler(handler)
        return handler
    
    def add_rotating_file_handler(
        self, 
        filename: str, 
        level: LogLevel = LogLevel.DEBUG, 
        formatter: Optional[Formatter] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        encoding: str = 'utf-8'
    ) -> RotatingFileHandler:
        """
        Add a rotating file handler to this logger.
        
        Args:
            filename: Path to the log file
            level: The minimum log level for the handler
            formatter: The formatter to use
            max_bytes: Maximum size of the log file before rotation
            backup_count: Number of backup files to keep
            encoding: File encoding
            
        Returns:
            The created handler
        """
        handler = RotatingFileHandler(filename, level, formatter, max_bytes, backup_count, encoding)
        self.add_handler(handler)
        return handler
    
    def add_network_handler(
        self, 
        host: str,
        port: int,
        endpoint: str = '/logs',
        level: LogLevel = LogLevel.ERROR,
        formatter: Optional[Formatter] = None,
        method: str = 'POST',
        secure: bool = True,
        async_mode: bool = True
    ) -> Union[NetworkHandler, AsyncHandler]:
        """
        Add a network handler to this logger.
        
        Args:
            host: The remote host to send logs to
            port: The port on the remote host
            endpoint: The endpoint URL path
            level: The minimum log level for the handler
            formatter: The formatter to use
            method: The HTTP method to use
            secure: Whether to use HTTPS
            async_mode: Whether to use asynchronous mode
            
        Returns:
            The created handler
        """
        # Use JSON formatter by default for network handlers
        if formatter is None:
            formatter = JsonFormatter()
        
        handler = NetworkHandler(host, port, endpoint, level, formatter, method, secure)
        
        if async_mode:
            # Wrap in an async handler to avoid blocking
            async_handler = AsyncHandler(handler)
            self.add_handler(async_handler)
            return async_handler
        else:
            self.add_handler(handler)
            return handler
    
    def context(self, **kwargs) -> 'LoggerContext':
        """
        Create a context manager for adding context to log records.
        
        Args:
            **kwargs: Context key-value pairs
            
        Returns:
            A context manager that adds the specified context to log records
        """
        return LoggerContext(self, kwargs)
    
    def close(self) -> None:
        """Close all handlers attached to this logger."""
        for handler in self.handlers:
            handler.close()


class LoggerContext:
    """
    A context manager for adding context to log records.
    
    This allows for structured logging with additional context that is
    automatically added to all log records within the context.
    """
    
    def __init__(self, logger: Logger, context: Dict[str, Any]):
        """
        Initialize the logger context.
        
        Args:
            logger: The logger to add context to
            context: The context key-value pairs
        """
        self.logger = logger
        self.context = context
    
    def __enter__(self) -> None:
        """Enter the context, adding the context to the logger's context stack."""
        with self.logger._context_lock:
            self.logger._context_stack.append(self.context)
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context, removing the context from the logger's context stack."""
        with self.logger._context_lock:
            if self.logger._context_stack:
                self.logger._context_stack.pop()

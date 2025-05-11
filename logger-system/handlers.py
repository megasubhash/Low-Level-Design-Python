import os
import sys
import time
import socket
import queue
import threading
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import http.client
import json

from log_level import LogLevel
from log_record import LogRecord
from formatters import Formatter, SimpleFormatter


class Handler(ABC):
    """
    Abstract base class for log handlers.
    
    Handlers are responsible for dispatching log records to specific destinations.
    """
    
    def __init__(self, level: LogLevel = LogLevel.DEBUG, formatter: Optional[Formatter] = None):
        """
        Initialize the handler.
        
        Args:
            level: The minimum log level this handler will process
            formatter: The formatter to use for formatting log records
        """
        self.level = level
        self.formatter = formatter or SimpleFormatter()
        self.filters: List[callable] = []
    
    def add_filter(self, filter_func: callable) -> None:
        """
        Add a filter function to this handler.
        
        Args:
            filter_func: A function that takes a LogRecord and returns a boolean
                        indicating whether the record should be processed.
        """
        self.filters.append(filter_func)
    
    def should_handle(self, record: LogRecord) -> bool:
        """
        Determine if this handler should handle the given record.
        
        Args:
            record: The log record to check
            
        Returns:
            True if the record should be handled, False otherwise
        """
        # Check if the record's level is high enough
        if record.level.value < self.level.value:
            return False
        
        # Apply all filters
        for filter_func in self.filters:
            if not filter_func(record):
                return False
        
        return True
    
    def handle(self, record: LogRecord) -> None:
        """
        Handle a log record.
        
        Args:
            record: The log record to handle
        """
        if self.should_handle(record):
            self.emit(record)
    
    @abstractmethod
    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record to the destination.
        
        Args:
            record: The log record to emit
        """
        pass
    
    def close(self) -> None:
        """Close the handler and release any resources."""
        pass


class ConsoleHandler(Handler):
    """Handler that writes log records to the console (stdout or stderr)."""
    
    def __init__(
        self, 
        level: LogLevel = LogLevel.DEBUG, 
        formatter: Optional[Formatter] = None,
        use_stderr_for_errors: bool = True
    ):
        """
        Initialize the console handler.
        
        Args:
            level: The minimum log level this handler will process
            formatter: The formatter to use for formatting log records
            use_stderr_for_errors: If True, ERROR and CRITICAL messages will be sent to stderr
        """
        super().__init__(level, formatter)
        self.use_stderr_for_errors = use_stderr_for_errors
    
    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record to the console.
        
        Args:
            record: The log record to emit
        """
        message = self.formatter.format(record)
        
        # Determine whether to use stdout or stderr
        if self.use_stderr_for_errors and record.level.value >= LogLevel.ERROR.value:
            stream = sys.stderr
        else:
            stream = sys.stdout
        
        stream.write(message + '\n')
        stream.flush()


class FileHandler(Handler):
    """Handler that writes log records to a file."""
    
    def __init__(
        self, 
        filename: str, 
        level: LogLevel = LogLevel.DEBUG, 
        formatter: Optional[Formatter] = None,
        mode: str = 'a',
        encoding: str = 'utf-8'
    ):
        """
        Initialize the file handler.
        
        Args:
            filename: Path to the log file
            level: The minimum log level this handler will process
            formatter: The formatter to use for formatting log records
            mode: File opening mode ('a' for append, 'w' for write)
            encoding: File encoding
        """
        super().__init__(level, formatter)
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None
        self._open()
    
    def _open(self) -> None:
        """Open the log file."""
        # Create directory if it doesn't exist
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        self.file = open(self.filename, self.mode, encoding=self.encoding)
    
    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record to the file.
        
        Args:
            record: The log record to emit
        """
        if self.file is None:
            self._open()
        
        message = self.formatter.format(record)
        self.file.write(message + '\n')
        self.file.flush()
    
    def close(self) -> None:
        """Close the log file."""
        if self.file:
            self.file.close()
            self.file = None


class RotatingFileHandler(FileHandler):
    """
    Handler that writes log records to a file, rotating the file when it reaches
    a certain size or at certain time intervals.
    """
    
    def __init__(
        self, 
        filename: str, 
        level: LogLevel = LogLevel.DEBUG, 
        formatter: Optional[Formatter] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        encoding: str = 'utf-8'
    ):
        """
        Initialize the rotating file handler.
        
        Args:
            filename: Path to the log file
            level: The minimum log level this handler will process
            formatter: The formatter to use for formatting log records
            max_bytes: Maximum size of the log file before rotation (in bytes)
            backup_count: Number of backup files to keep
            encoding: File encoding
        """
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        super().__init__(filename, level, formatter, 'a', encoding)
    
    def should_rollover(self) -> bool:
        """
        Determine if the log file should be rolled over.
        
        Returns:
            True if the file should be rolled over, False otherwise
        """
        if self.max_bytes <= 0:
            return False
        
        if self.file.tell() >= self.max_bytes:
            return True
        
        return False
    
    def do_rollover(self) -> None:
        """Perform log file rotation."""
        if self.file:
            self.file.close()
            self.file = None
        
        # If backup_count is 0, just delete the file
        if self.backup_count == 0:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        else:
            # Shift existing log files
            for i in range(self.backup_count - 1, 0, -1):
                src = f"{self.filename}.{i}"
                dst = f"{self.filename}.{i + 1}"
                
                if os.path.exists(src):
                    if os.path.exists(dst):
                        os.remove(dst)
                    os.rename(src, dst)
            
            # Rename the current log file
            if os.path.exists(self.filename):
                os.rename(self.filename, f"{self.filename}.1")
        
        # Open a new file
        self._open()
    
    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record to the file, rotating if necessary.
        
        Args:
            record: The log record to emit
        """
        if self.should_rollover():
            self.do_rollover()
        
        super().emit(record)


class NetworkHandler(Handler):
    """Handler that sends log records to a remote server over HTTP/HTTPS."""
    
    def __init__(
        self, 
        host: str,
        port: int,
        endpoint: str = '/logs',
        level: LogLevel = LogLevel.ERROR,
        formatter: Optional[Formatter] = None,
        method: str = 'POST',
        secure: bool = True,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 5
    ):
        """
        Initialize the network handler.
        
        Args:
            host: The remote host to send logs to
            port: The port on the remote host
            endpoint: The endpoint URL path
            level: The minimum log level this handler will process
            formatter: The formatter to use for formatting log records
            method: The HTTP method to use ('POST' or 'PUT')
            secure: Whether to use HTTPS (True) or HTTP (False)
            headers: Additional HTTP headers to include in the request
            timeout: Connection timeout in seconds
        """
        super().__init__(level, formatter)
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.method = method
        self.secure = secure
        self.headers = headers or {'Content-Type': 'application/json'}
        self.timeout = timeout
    
    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record to the remote server.
        
        Args:
            record: The log record to emit
        """
        try:
            # Format the record
            message = self.formatter.format(record)
            
            # Create connection
            if self.secure:
                conn = http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout)
            else:
                conn = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            
            # Send request
            conn.request(
                self.method,
                self.endpoint,
                message,
                self.headers
            )
            
            # Get response (but don't wait for it)
            conn.getresponse()
            
        except Exception as e:
            # Don't raise exceptions from the logger
            sys.stderr.write(f"Error sending log to network: {e}\n")
        finally:
            if 'conn' in locals():
                conn.close()


class AsyncHandler(Handler):
    """
    A handler that processes log records asynchronously in a separate thread.
    
    This is useful for handlers that might block, such as network or database handlers.
    """
    
    def __init__(
        self, 
        handler: Handler,
        queue_size: int = 1000
    ):
        """
        Initialize the async handler.
        
        Args:
            handler: The underlying handler to use for actual log processing
            queue_size: Maximum number of log records to queue before blocking
        """
        super().__init__(handler.level, handler.formatter)
        self.handler = handler
        self.queue = queue.Queue(maxsize=queue_size)
        self.thread = threading.Thread(target=self._process_queue, daemon=True)
        self.thread.start()
        self.is_running = True
    
    def _process_queue(self) -> None:
        """Process log records from the queue in a separate thread."""
        while self.is_running:
            try:
                # Get a record from the queue, waiting up to 0.1 seconds
                record = self.queue.get(block=True, timeout=0.1)
                
                # Process the record with the underlying handler
                self.handler.handle(record)
                
                # Mark the task as done
                self.queue.task_done()
                
            except queue.Empty:
                # No records in the queue, just continue
                continue
            except Exception as e:
                # Don't let exceptions kill the thread
                sys.stderr.write(f"Error in async handler: {e}\n")
    
    def emit(self, record: LogRecord) -> None:
        """
        Queue a log record for asynchronous processing.
        
        Args:
            record: The log record to emit
        """
        try:
            self.queue.put(record, block=False)
        except queue.Full:
            sys.stderr.write("Async handler queue is full, dropping log record\n")
    
    def close(self) -> None:
        """Close the handler and wait for the queue to be processed."""
        self.is_running = False
        
        # Wait for the thread to finish processing the queue
        if self.thread.is_alive():
            self.thread.join(timeout=5.0)
        
        # Close the underlying handler
        self.handler.close()

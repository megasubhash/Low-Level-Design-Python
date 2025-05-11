import time
import uuid
import threading
import traceback
import socket
import os
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from log_level import LogLevel


@dataclass
class LogRecord:
    """
    Represents a single log record with all relevant information.
    
    This class encapsulates all information related to a single logging event,
    including the original logger name, log level, message, timestamp, and
    any additional contextual information.
    """
    logger_name: str
    level: LogLevel
    message: str
    timestamp: float = field(default_factory=time.time)
    thread_id: int = field(default_factory=threading.get_ident)
    thread_name: str = field(default_factory=lambda: threading.current_thread().name)
    process_id: int = field(default_factory=os.getpid)
    hostname: str = field(default_factory=socket.gethostname)
    context: Dict[str, Any] = field(default_factory=dict)
    exception_info: Optional[tuple] = None
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        """Ensure level is a LogLevel enum."""
        if isinstance(self.level, int):
            # Convert integer level to LogLevel enum
            for level in LogLevel:
                if level.value == self.level:
                    self.level = level
                    break
        elif isinstance(self.level, str):
            # Convert string level to LogLevel enum
            self.level = LogLevel.from_string(self.level)
    
    @property
    def level_name(self) -> str:
        """Get the name of the log level."""
        return self.level.name
    
    @property
    def formatted_timestamp(self) -> str:
        """Get the timestamp formatted as a string."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
    
    def get_formatted_exception(self) -> Optional[str]:
        """Format exception information as a string if available."""
        if self.exception_info:
            return ''.join(traceback.format_exception(*self.exception_info))
        return None
    
    def add_context(self, **kwargs) -> None:
        """Add additional context information to the log record."""
        self.context.update(kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the log record to a dictionary."""
        result = {
            'record_id': self.record_id,
            'logger_name': self.logger_name,
            'level': self.level.value,
            'level_name': self.level_name,
            'message': self.message,
            'timestamp': self.timestamp,
            'formatted_timestamp': self.formatted_timestamp,
            'thread_id': self.thread_id,
            'thread_name': self.thread_name,
            'process_id': self.process_id,
            'hostname': self.hostname,
            'context': self.context,
        }
        
        if self.exception_info:
            result['exception'] = self.get_formatted_exception()
            
        return result

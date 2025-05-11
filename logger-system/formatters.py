from abc import ABC, abstractmethod
import json
from typing import Dict, Any

from log_record import LogRecord


class Formatter(ABC):
    """
    Abstract base class for log formatters.
    
    Formatters are responsible for converting a LogRecord into a string
    representation suitable for output by a Handler.
    """
    
    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Format a LogRecord into a string."""
        pass


class SimpleFormatter(Formatter):
    """
    A simple formatter that produces log messages in a standard format.
    
    Format: [TIMESTAMP] [LEVEL] [LOGGER] - MESSAGE
    """
    
    def format(self, record: LogRecord) -> str:
        """Format a LogRecord into a simple string."""
        base_msg = f"[{record.formatted_timestamp}] [{record.level_name}] [{record.logger_name}] - {record.message}"
        
        # Add exception information if available
        exception_info = record.get_formatted_exception()
        if exception_info:
            base_msg += f"\n{exception_info}"
            
        # Add context information if available
        if record.context:
            context_str = ", ".join(f"{k}={v}" for k, v in record.context.items())
            base_msg += f" ({context_str})"
            
        return base_msg


class DetailedFormatter(Formatter):
    """
    A more detailed formatter that includes thread and process information.
    
    Format: [TIMESTAMP] [LEVEL] [LOGGER] [THREAD:thread_id] [PROCESS:process_id] - MESSAGE
    """
    
    def format(self, record: LogRecord) -> str:
        """Format a LogRecord into a detailed string."""
        base_msg = (
            f"[{record.formatted_timestamp}] [{record.level_name}] [{record.logger_name}] "
            f"[THREAD:{record.thread_name}:{record.thread_id}] [PROCESS:{record.process_id}] - {record.message}"
        )
        
        # Add exception information if available
        exception_info = record.get_formatted_exception()
        if exception_info:
            base_msg += f"\n{exception_info}"
            
        # Add context information if available
        if record.context:
            context_str = ", ".join(f"{k}={v}" for k, v in record.context.items())
            base_msg += f" ({context_str})"
            
        return base_msg


class JsonFormatter(Formatter):
    """
    A formatter that produces JSON-formatted log messages.
    
    This is useful for structured logging and log aggregation systems.
    """
    
    def __init__(self, indent: int = None):
        """
        Initialize the JSON formatter.
        
        Args:
            indent: Number of spaces for indentation in the JSON output.
                   If None, the JSON will be compact.
        """
        self.indent = indent
    
    def format(self, record: LogRecord) -> str:
        """Format a LogRecord into a JSON string."""
        return json.dumps(record.to_dict(), indent=self.indent)


class CustomFormatter(Formatter):
    """
    A customizable formatter that uses a format string with placeholders.
    
    Format strings can include any attribute of the LogRecord using {attribute} syntax.
    """
    
    def __init__(self, format_string: str):
        """
        Initialize the custom formatter with a format string.
        
        Args:
            format_string: A string with {attribute} placeholders.
                          Example: "{formatted_timestamp} - {level_name}: {message}"
        """
        self.format_string = format_string
    
    def format(self, record: LogRecord) -> str:
        """Format a LogRecord using the custom format string."""
        # Create a dictionary with all attributes from the record
        data = record.to_dict()
        
        # Add exception information if available
        exception_info = record.get_formatted_exception()
        if exception_info:
            data['exception'] = exception_info
        
        try:
            return self.format_string.format(**data)
        except KeyError as e:
            # If a placeholder in the format string doesn't match any attribute
            return f"[FORMATTER ERROR: Invalid placeholder {e}] {record.message}"

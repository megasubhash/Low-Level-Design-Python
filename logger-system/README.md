# Logger System - Low Level Design

This project implements a flexible, extensible logging system in Python that follows SOLID principles and design patterns. The logger system provides a robust framework for application logging with features like different log levels, multiple output destinations, formatting options, and more.

## Features

- **Multiple Log Levels**: Support for standard log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Configurable Outputs**: Log to console, files, network, or custom destinations
- **Flexible Formatting**: Customizable log message formats
- **Asynchronous Logging**: Non-blocking logging for high-performance applications
- **Log Rotation**: Automatic log file rotation based on size or time
- **Context-based Logging**: Capture contextual information (thread ID, request ID, etc.)
- **Filtering**: Filter logs based on various criteria
- **Extensibility**: Easy to extend with custom formatters, handlers, and filters

## Architecture

The logger system follows a modular architecture with the following components:

1. **Logger**: The main entry point for logging messages
2. **LogLevel**: Enumeration of different log severity levels
3. **LogRecord**: Contains all information about a single log event
4. **Handler**: Responsible for sending log records to specific destinations
5. **Formatter**: Formats log records into strings
6. **Filter**: Determines which log records to process
7. **LoggerFactory**: Creates and manages logger instances

## Design Patterns Used

- **Singleton**: For the LoggerFactory to ensure a single point of access
- **Factory Method**: For creating different types of loggers and handlers
- **Strategy**: For different formatting and output strategies
- **Chain of Responsibility**: For log record processing through filters and handlers
- **Observer**: For notification of log events
- **Decorator**: For adding additional functionality to loggers

## Usage Example

```python
from logger_system import LoggerFactory, LogLevel

# Get a logger instance
logger = LoggerFactory.get_logger("app")

# Configure the logger
logger.add_console_handler(LogLevel.INFO)
logger.add_file_handler("app.log", LogLevel.DEBUG)

# Log messages
logger.debug("This is a debug message")
logger.info("Application started")
logger.warning("Resource usage high")
logger.error("Failed to connect to database")
logger.critical("System shutdown initiated")

# Using context manager for structured logging
with logger.context(request_id="12345", user="admin"):
    logger.info("Processing request")
```

## Implementation Details

The system is designed to be thread-safe and efficient, with minimal overhead for applications. It provides both synchronous and asynchronous logging capabilities to suit different performance requirements.

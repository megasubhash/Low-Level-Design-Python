from enum import Enum, auto


class LogLevel(Enum):
    """
    Enumeration of log levels in increasing order of severity.
    
    Attributes:
        DEBUG: Detailed information, typically of interest only when diagnosing problems.
        INFO: Confirmation that things are working as expected.
        WARNING: An indication that something unexpected happened, or may happen in the near future.
        ERROR: Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
    """
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    
    @classmethod
    def get_level_name(cls, level):
        """Get the name of a log level."""
        for level_name, level_value in cls.__members__.items():
            if level_value.value == level:
                return level_name
        return f"Level {level}"
    
    @classmethod
    def from_string(cls, level_name):
        """Convert a string level name to the corresponding LogLevel."""
        try:
            return cls[level_name.upper()]
        except KeyError:
            raise ValueError(f"Invalid log level: {level_name}")

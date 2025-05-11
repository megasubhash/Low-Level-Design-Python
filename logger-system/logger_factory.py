import os
import json
import threading
from typing import Dict, Optional, List, Any

from log_level import LogLevel
from logger import Logger
from formatters import SimpleFormatter, DetailedFormatter, JsonFormatter, CustomFormatter
from handlers import ConsoleHandler, FileHandler, RotatingFileHandler, NetworkHandler, AsyncHandler


class LoggerFactory:
    """
    Factory class for creating and managing logger instances.
    
    This class implements the Singleton pattern to ensure that there is only
    one instance of the factory throughout the application.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Create a new instance of LoggerFactory if one doesn't exist."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LoggerFactory, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the logger factory."""
        self.loggers: Dict[str, Logger] = {}
        self.root_logger = self._create_logger("root")
        self.config_file: Optional[str] = None
    
    @classmethod
    def get_instance(cls) -> 'LoggerFactory':
        """
        Get the singleton instance of LoggerFactory.
        
        Returns:
            The LoggerFactory instance
        """
        if cls._instance is None:
            return cls()
        return cls._instance
    
    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """
        Get a logger with the specified name.
        
        If a logger with the name already exists, it will be returned.
        Otherwise, a new logger will be created.
        
        Args:
            name: The name of the logger
            
        Returns:
            The logger instance
        """
        factory = cls.get_instance()
        
        # Check if the logger already exists
        if name in factory.loggers:
            return factory.loggers[name]
        
        # Create a new logger
        logger = factory._create_logger(name)
        
        # Set up parent-child relationships
        if name != "root":
            # Find the parent logger
            parent_name = name.rsplit(".", 1)[0] if "." in name else "root"
            parent_logger = cls.get_logger(parent_name)
            logger.parent = parent_logger
        
        return logger
    
    def _create_logger(self, name: str) -> Logger:
        """
        Create a new logger with the specified name.
        
        Args:
            name: The name of the logger
            
        Returns:
            The created logger
        """
        logger = Logger(name)
        self.loggers[name] = logger
        return logger
    
    @classmethod
    def configure_from_file(cls, config_file: str) -> None:
        """
        Configure loggers from a JSON configuration file.
        
        Args:
            config_file: Path to the configuration file
        """
        factory = cls.get_instance()
        factory.config_file = config_file
        
        # Check if the file exists
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        # Load the configuration
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Configure loggers
        factory._configure_from_dict(config)
    
    @classmethod
    def configure_from_dict(cls, config: Dict[str, Any]) -> None:
        """
        Configure loggers from a dictionary.
        
        Args:
            config: Configuration dictionary
        """
        factory = cls.get_instance()
        factory._configure_from_dict(config)
    
    def _configure_from_dict(self, config: Dict[str, Any]) -> None:
        """
        Configure loggers from a dictionary.
        
        Args:
            config: Configuration dictionary
        """
        # Configure root logger
        if "root" in config:
            self._configure_logger("root", config["root"])
        
        # Configure other loggers
        if "loggers" in config:
            for name, logger_config in config["loggers"].items():
                self._configure_logger(name, logger_config)
    
    def _configure_logger(self, name: str, config: Dict[str, Any]) -> None:
        """
        Configure a logger from a dictionary.
        
        Args:
            name: The name of the logger
            config: Configuration dictionary for the logger
        """
        # Get or create the logger
        logger = self.get_logger(name)
        
        # Set the log level
        if "level" in config:
            level_str = config["level"].upper()
            try:
                level = LogLevel[level_str]
                logger.set_level(level)
            except KeyError:
                pass
        
        # Configure propagation
        if "propagate" in config:
            logger.propagate = bool(config["propagate"])
        
        # Configure handlers
        if "handlers" in config:
            for handler_config in config["handlers"]:
                handler_type = handler_config.get("type", "console")
                
                if handler_type == "console":
                    self._configure_console_handler(logger, handler_config)
                elif handler_type == "file":
                    self._configure_file_handler(logger, handler_config)
                elif handler_type == "rotating_file":
                    self._configure_rotating_file_handler(logger, handler_config)
                elif handler_type == "network":
                    self._configure_network_handler(logger, handler_config)
    
    def _get_formatter(self, config: Dict[str, Any]):
        """
        Create a formatter from a configuration dictionary.
        
        Args:
            config: Configuration dictionary for the formatter
            
        Returns:
            The created formatter
        """
        formatter_type = config.get("formatter", "simple")
        
        if formatter_type == "simple":
            return SimpleFormatter()
        elif formatter_type == "detailed":
            return DetailedFormatter()
        elif formatter_type == "json":
            indent = config.get("indent")
            return JsonFormatter(indent)
        elif formatter_type == "custom":
            format_string = config.get("format", "{formatted_timestamp} - {level_name}: {message}")
            return CustomFormatter(format_string)
        else:
            return SimpleFormatter()
    
    def _get_log_level(self, config: Dict[str, Any], default: LogLevel = LogLevel.INFO):
        """
        Get a log level from a configuration dictionary.
        
        Args:
            config: Configuration dictionary
            default: Default log level if not specified
            
        Returns:
            The log level
        """
        if "level" in config:
            level_str = config["level"].upper()
            try:
                return LogLevel[level_str]
            except KeyError:
                pass
        return default
    
    def _configure_console_handler(self, logger: Logger, config: Dict[str, Any]) -> None:
        """
        Configure a console handler for a logger.
        
        Args:
            logger: The logger to configure
            config: Configuration dictionary for the handler
        """
        level = self._get_log_level(config)
        formatter = self._get_formatter(config)
        use_stderr = config.get("use_stderr_for_errors", True)
        
        logger.add_console_handler(level, formatter, use_stderr)
    
    def _configure_file_handler(self, logger: Logger, config: Dict[str, Any]) -> None:
        """
        Configure a file handler for a logger.
        
        Args:
            logger: The logger to configure
            config: Configuration dictionary for the handler
        """
        if "filename" not in config:
            return
        
        filename = config["filename"]
        level = self._get_log_level(config)
        formatter = self._get_formatter(config)
        mode = config.get("mode", "a")
        encoding = config.get("encoding", "utf-8")
        
        logger.add_file_handler(filename, level, formatter, mode, encoding)
    
    def _configure_rotating_file_handler(self, logger: Logger, config: Dict[str, Any]) -> None:
        """
        Configure a rotating file handler for a logger.
        
        Args:
            logger: The logger to configure
            config: Configuration dictionary for the handler
        """
        if "filename" not in config:
            return
        
        filename = config["filename"]
        level = self._get_log_level(config)
        formatter = self._get_formatter(config)
        max_bytes = config.get("max_bytes", 10 * 1024 * 1024)  # 10 MB
        backup_count = config.get("backup_count", 5)
        encoding = config.get("encoding", "utf-8")
        
        logger.add_rotating_file_handler(filename, level, formatter, max_bytes, backup_count, encoding)
    
    def _configure_network_handler(self, logger: Logger, config: Dict[str, Any]) -> None:
        """
        Configure a network handler for a logger.
        
        Args:
            logger: The logger to configure
            config: Configuration dictionary for the handler
        """
        if "host" not in config or "port" not in config:
            return
        
        host = config["host"]
        port = config["port"]
        endpoint = config.get("endpoint", "/logs")
        level = self._get_log_level(config, LogLevel.ERROR)
        formatter = self._get_formatter(config)
        method = config.get("method", "POST")
        secure = config.get("secure", True)
        async_mode = config.get("async", True)
        
        logger.add_network_handler(host, port, endpoint, level, formatter, method, secure, async_mode)
    
    @classmethod
    def shutdown(cls) -> None:
        """Close all loggers and their handlers."""
        factory = cls.get_instance()
        for logger in factory.loggers.values():
            logger.close()

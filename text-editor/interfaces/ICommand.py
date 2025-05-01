from abc import ABC, abstractmethod

class ICommand(ABC):
    """Interface for command pattern implementation."""
    
    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the command."""
        pass

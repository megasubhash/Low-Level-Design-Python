from abc import ABC, abstractmethod

class IPartitionStrategy(ABC):
    """Interface for message partition strategies."""
    
    @abstractmethod
    def assign_partition(self, message, topic):
        """
        Assign a partition to a message.
        
        Args:
            message: The message to assign a partition to
            topic: The topic the message belongs to
            
        Returns:
            int: Partition ID to assign
        """
        pass

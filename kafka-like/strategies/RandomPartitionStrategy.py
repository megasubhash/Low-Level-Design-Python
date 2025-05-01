import random
from interfaces.IPartitionStrategy import IPartitionStrategy

class RandomPartitionStrategy(IPartitionStrategy):
    """
    A partition strategy that randomly assigns messages to partitions.
    
    This strategy provides a simple way to distribute messages across partitions
    without considering message keys or maintaining state.
    """
    
    def assign_partition(self, message, topic):
        """
        Assign a partition to a message randomly.
        
        Args:
            message: The message to assign a partition to
            topic: The topic the message belongs to
            
        Returns:
            int: Partition ID to assign
        """
        # Randomly select a partition from the available partitions
        return random.randint(0, topic.num_partitions - 1)

from interfaces.IPartitionStrategy import IPartitionStrategy

class RoundRobinPartitionStrategy(IPartitionStrategy):
    """
    A partition strategy that distributes messages evenly across partitions.
    
    This strategy assigns partitions in a round-robin fashion, cycling through all available
    partitions sequentially.
    """
    
    def __init__(self):
        """Initialize the RoundRobinPartitionStrategy."""
        self.next_partition = {}  # Map of topic_name to next partition to use
    
    def assign_partition(self, message, topic):
        """
        Assign a partition to a message using round-robin strategy.
        
        Args:
            message: The message to assign a partition to
            topic: The topic the message belongs to
            
        Returns:
            int: Partition ID to assign
        """
        topic_name = topic.name
        
        # Get the next partition for this topic
        if topic_name not in self.next_partition:
            self.next_partition[topic_name] = 0
        
        # Assign the current partition
        partition_id = self.next_partition[topic_name]
        
        # Update the next partition (cycle through available partitions)
        self.next_partition[topic_name] = (partition_id + 1) % topic.num_partitions
        
        return partition_id

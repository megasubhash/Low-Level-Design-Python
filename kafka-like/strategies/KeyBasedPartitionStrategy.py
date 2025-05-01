import hashlib
from interfaces.IPartitionStrategy import IPartitionStrategy

class KeyBasedPartitionStrategy(IPartitionStrategy):
    """
    A partition strategy that uses the message key to determine the partition.
    
    This strategy ensures that messages with the same key always go to the same partition,
    which guarantees ordering for messages with the same key.
    """
    
    def assign_partition(self, message, topic):
        """
        Assign a partition to a message based on its key.
        
        Args:
            message: The message to assign a partition to
            topic: The topic the message belongs to
            
        Returns:
            int: Partition ID to assign
        """
        # If no key is provided, use a default partition
        if not message.key:
            return 0
        
        # Hash the key to determine the partition
        key_bytes = message.key.encode('utf-8')
        key_hash = int(hashlib.md5(key_bytes).hexdigest(), 16)
        
        # Use modulo to get a partition within the valid range
        return key_hash % topic.num_partitions

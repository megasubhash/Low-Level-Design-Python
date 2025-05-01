from models.Partition import Partition

class Topic:
    """Represents a topic in the pub-sub system."""
    
    def __init__(self, name, num_partitions=1, replication_factor=1):
        """
        Initialize a Topic object.
        
        Args:
            name (str): Topic name
            num_partitions (int): Number of partitions for this topic
            replication_factor (int): Replication factor for this topic
        """
        self.name = name
        self.num_partitions = num_partitions
        self.replication_factor = replication_factor
        self.partitions = {}  # Map of partition_id to Partition
        
        # Create partitions
        for i in range(num_partitions):
            self.partitions[i] = Partition(i, name)
    
    def __str__(self):
        return f"Topic(name={self.name}, partitions={self.num_partitions}, replication={self.replication_factor})"
    
    def get_partition(self, partition_id):
        """
        Get a partition by ID.
        
        Args:
            partition_id (int): ID of the partition
            
        Returns:
            Partition: The partition, or None if not found
        """
        return self.partitions.get(partition_id)
    
    def get_all_partitions(self):
        """
        Get all partitions for this topic.
        
        Returns:
            list: List of all partitions
        """
        return list(self.partitions.values())

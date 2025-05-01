class Partition:
    """Represents a partition within a topic."""
    
    def __init__(self, partition_id, topic_name):
        """
        Initialize a Partition object.
        
        Args:
            partition_id (int): Partition identifier
            topic_name (str): Name of the topic this partition belongs to
        """
        self.id = partition_id
        self.topic_name = topic_name
        self.messages = []  # List of messages in this partition
        self.next_offset = 0  # Next offset to assign
        
    def __str__(self):
        return f"Partition(id={self.id}, topic={self.topic_name}, messages={len(self.messages)})"
    
    def add_message(self, message):
        """
        Add a message to this partition.
        
        Args:
            message (Message): Message to add
            
        Returns:
            int: Offset assigned to the message
        """
        # Assign offset to message
        offset = self.next_offset
        message.set_delivered(self.id, offset)
        
        # Add message to partition
        self.messages.append(message)
        
        # Increment next offset
        self.next_offset += 1
        
        return offset
    
    def get_message(self, offset):
        """
        Get a message by offset.
        
        Args:
            offset (int): Offset of the message
            
        Returns:
            Message: The message at the offset, or None if not found
        """
        if offset < 0 or offset >= len(self.messages):
            return None
        
        return self.messages[offset]
    
    def get_messages(self, start_offset=0, max_count=None):
        """
        Get messages starting from an offset.
        
        Args:
            start_offset (int): Starting offset
            max_count (int, optional): Maximum number of messages to return
            
        Returns:
            list: List of messages
        """
        if start_offset < 0 or start_offset >= len(self.messages):
            return []
        
        if max_count is None:
            return self.messages[start_offset:]
        
        end_offset = min(start_offset + max_count, len(self.messages))
        return self.messages[start_offset:end_offset]

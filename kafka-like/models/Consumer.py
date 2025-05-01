import uuid

class Consumer:
    """Represents a message consumer in the pub-sub system."""
    
    def __init__(self, consumer_id=None, group_id=None, broker=None):
        """
        Initialize a Consumer object.
        
        Args:
            consumer_id (str, optional): Unique identifier for the consumer
            group_id (str, optional): Consumer group ID
            broker: Broker to consume messages from
        """
        self.id = consumer_id or str(uuid.uuid4())
        self.group_id = group_id or str(uuid.uuid4())
        self.broker = broker
        self.subscribed_topics = set()  # Set of subscribed topic names
        self.offsets = {}  # Map of (topic, partition) to current offset
        self.consumed_messages = []  # List of consumed message IDs
    
    def __str__(self):
        return f"Consumer(id={self.id}, group={self.group_id}, subscribed_topics={len(self.subscribed_topics)})"
    
    def subscribe(self, topic_name):
        """
        Subscribe to a topic.
        
        Args:
            topic_name (str): Name of the topic to subscribe to
            
        Returns:
            bool: True if subscription was successful, False otherwise
        """
        if not self.broker:
            return False
        
        # Check if topic exists
        if not self.broker.topic_exists(topic_name):
            return False
        
        # Add to subscribed topics
        self.subscribed_topics.add(topic_name)
        
        # Initialize offsets for this topic
        topic = self.broker.get_topic(topic_name)
        for partition_id in topic.partitions:
            self.offsets[(topic_name, partition_id)] = 0
        
        return True
    
    def unsubscribe(self, topic_name):
        """
        Unsubscribe from a topic.
        
        Args:
            topic_name (str): Name of the topic to unsubscribe from
            
        Returns:
            bool: True if unsubscription was successful, False otherwise
        """
        if topic_name in self.subscribed_topics:
            self.subscribed_topics.remove(topic_name)
            
            # Remove offsets for this topic
            for key in list(self.offsets.keys()):
                if key[0] == topic_name:
                    del self.offsets[key]
            
            return True
        
        return False
    
    def poll(self, max_messages=1):
        """
        Poll for messages from subscribed topics.
        
        Args:
            max_messages (int): Maximum number of messages to retrieve
            
        Returns:
            list: List of retrieved messages
        """
        if not self.broker:
            return []
        
        messages = []
        
        # Poll each subscribed topic
        for topic_name in self.subscribed_topics:
            topic = self.broker.get_topic(topic_name)
            
            # Poll each partition
            for partition_id, partition in topic.partitions.items():
                # Get current offset for this partition
                current_offset = self.offsets.get((topic_name, partition_id), 0)
                
                # Get messages from this partition
                partition_messages = partition.get_messages(current_offset, max_messages - len(messages))
                
                if partition_messages:
                    messages.extend(partition_messages)
                    
                    # Update offset
                    self.offsets[(topic_name, partition_id)] = current_offset + len(partition_messages)
                    
                    # Mark messages as consumed
                    for message in partition_messages:
                        message.set_consumed()
                        self.consumed_messages.append(message.id)
                
                # Stop if we have enough messages
                if len(messages) >= max_messages:
                    break
            
            # Stop if we have enough messages
            if len(messages) >= max_messages:
                break
        
        return messages
    
    def commit_offsets(self):
        """
        Commit current offsets to the broker.
        
        Returns:
            bool: True if commit was successful, False otherwise
        """
        if not self.broker:
            return False
        
        # In a real system, this would persist the offsets to the broker
        # For simplicity, we'll just return True
        return True
    
    def set_broker(self, broker):
        """
        Set the broker for this consumer.
        
        Args:
            broker: Broker to consume messages from
        """
        self.broker = broker

import uuid

class Producer:
    """Represents a message producer in the pub-sub system."""
    
    def __init__(self, producer_id=None, broker=None):
        """
        Initialize a Producer object.
        
        Args:
            producer_id (str, optional): Unique identifier for the producer
            broker: Broker to send messages to
        """
        self.id = producer_id or str(uuid.uuid4())
        self.broker = broker
        self.sent_messages = []  # List of sent message IDs
    
    def __str__(self):
        return f"Producer(id={self.id}, messages_sent={len(self.sent_messages)})"
    
    def send(self, topic, value, key=None):
        """
        Send a message to a topic.
        
        Args:
            topic (str): Topic to send message to
            value (str): Message content
            key (str, optional): Message key for partitioning
            
        Returns:
            str: ID of the sent message, or None if failed
        """
        if not self.broker:
            return None
        
        # Send message to broker
        message_id = self.broker.send_message(topic, value, key, self.id)
        
        if message_id:
            self.sent_messages.append(message_id)
        
        return message_id
    
    def set_broker(self, broker):
        """
        Set the broker for this producer.
        
        Args:
            broker: Broker to send messages to
        """
        self.broker = broker

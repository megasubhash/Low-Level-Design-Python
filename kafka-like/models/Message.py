import uuid
from datetime import datetime
from enums.MessageStatus import MessageStatus

class Message:
    """Represents a message in the pub-sub system."""
    
    def __init__(self, message_id=None, topic=None, key=None, value=None, timestamp=None):
        """
        Initialize a Message object.
        
        Args:
            message_id (str, optional): Unique identifier for the message
            topic (str): Topic the message belongs to
            key (str, optional): Message key for partitioning
            value (str): Message content
            timestamp (datetime, optional): When the message was created
        """
        self.id = message_id or str(uuid.uuid4())
        self.topic = topic
        self.key = key
        self.value = value
        self.timestamp = timestamp or datetime.now()
        self.status = MessageStatus.PENDING
        self.partition = None  # Will be assigned by the broker
        self.offset = None     # Will be assigned by the broker
        
    def __str__(self):
        return (f"Message(id={self.id}, topic={self.topic}, key={self.key}, "
                f"partition={self.partition}, offset={self.offset}, "
                f"status={self.status.value})")
    
    def set_delivered(self, partition, offset):
        """
        Mark message as delivered and set partition and offset.
        
        Args:
            partition (int): Partition the message was assigned to
            offset (int): Offset within the partition
        """
        self.status = MessageStatus.DELIVERED
        self.partition = partition
        self.offset = offset
        
    def set_consumed(self):
        """Mark message as consumed."""
        self.status = MessageStatus.CONSUMED
        
    def set_failed(self):
        """Mark message as failed."""
        self.status = MessageStatus.FAILED

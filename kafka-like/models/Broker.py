import uuid
from models.Message import Message
from models.Topic import Topic
from enums.PartitionStrategy import PartitionStrategy
from factory.PartitionStrategyFactory import PartitionStrategyFactory

class Broker:
    """Represents a message broker in the pub-sub system."""
    
    def __init__(self, broker_id=None, partition_strategy_type=PartitionStrategy.ROUND_ROBIN):
        """
        Initialize a Broker object.
        
        Args:
            broker_id (str, optional): Unique identifier for the broker
            partition_strategy_type (PartitionStrategy): Strategy for partitioning messages
        """
        self.id = broker_id or str(uuid.uuid4())
        self.topics = {}  # Map of topic_name to Topic
        self.producers = {}  # Map of producer_id to Producer
        self.consumers = {}  # Map of consumer_id to Consumer
        self.consumer_groups = {}  # Map of group_id to set of consumer_ids
        
        # Set partition strategy
        factory = PartitionStrategyFactory()
        self.partition_strategy = factory.create_strategy(partition_strategy_type)
    
    def __str__(self):
        return (f"Broker(id={self.id}, topics={len(self.topics)}, "
                f"producers={len(self.producers)}, consumers={len(self.consumers)})")
    
    def create_topic(self, name, num_partitions=1, replication_factor=1):
        """
        Create a new topic.
        
        Args:
            name (str): Topic name
            num_partitions (int): Number of partitions for this topic
            replication_factor (int): Replication factor for this topic
            
        Returns:
            bool: True if topic was created, False if it already exists
        """
        if name in self.topics:
            return False
        
        # Create topic
        topic = Topic(name, num_partitions, replication_factor)
        self.topics[name] = topic
        
        return True
    
    def delete_topic(self, name):
        """
        Delete a topic.
        
        Args:
            name (str): Topic name
            
        Returns:
            bool: True if topic was deleted, False if it doesn't exist
        """
        if name in self.topics:
            del self.topics[name]
            return True
        
        return False
    
    def topic_exists(self, name):
        """
        Check if a topic exists.
        
        Args:
            name (str): Topic name
            
        Returns:
            bool: True if topic exists, False otherwise
        """
        return name in self.topics
    
    def get_topic(self, name):
        """
        Get a topic by name.
        
        Args:
            name (str): Topic name
            
        Returns:
            Topic: The topic, or None if not found
        """
        return self.topics.get(name)
    
    def register_producer(self, producer):
        """
        Register a producer with this broker.
        
        Args:
            producer (Producer): Producer to register
            
        Returns:
            bool: True if registration was successful
        """
        self.producers[producer.id] = producer
        producer.set_broker(self)
        return True
    
    def register_consumer(self, consumer):
        """
        Register a consumer with this broker.
        
        Args:
            consumer (Consumer): Consumer to register
            
        Returns:
            bool: True if registration was successful
        """
        self.consumers[consumer.id] = consumer
        consumer.set_broker(self)
        
        # Add to consumer group
        if consumer.group_id not in self.consumer_groups:
            self.consumer_groups[consumer.group_id] = set()
        
        self.consumer_groups[consumer.group_id].add(consumer.id)
        
        return True
    
    def send_message(self, topic_name, value, key=None, producer_id=None):
        """
        Send a message to a topic.
        
        Args:
            topic_name (str): Topic to send message to
            value (str): Message content
            key (str, optional): Message key for partitioning
            producer_id (str, optional): ID of the producer sending the message
            
        Returns:
            str: ID of the sent message, or None if failed
        """
        # Check if topic exists
        if topic_name not in self.topics:
            return None
        
        # Check if producer exists (if provided)
        if producer_id and producer_id not in self.producers:
            return None
        
        # Create message
        message = Message(topic=topic_name, key=key, value=value)
        
        # Get topic
        topic = self.topics[topic_name]
        
        # Assign partition using strategy
        partition_id = self.partition_strategy.assign_partition(message, topic)
        
        # Get partition
        partition = topic.get_partition(partition_id)
        
        # Add message to partition
        partition.add_message(message)
        
        return message.id
    
    def get_all_topics(self):
        """
        Get all topics.
        
        Returns:
            list: List of all topics
        """
        return list(self.topics.values())

from models.Broker import Broker
from models.Producer import Producer
from models.Consumer import Consumer
from enums.PartitionStrategy import PartitionStrategy

class MessageBrokerService:
    """Service for managing the message broker system."""
    
    def __init__(self, partition_strategy_type=PartitionStrategy.ROUND_ROBIN):
        """
        Initialize a MessageBrokerService.
        
        Args:
            partition_strategy_type (PartitionStrategy): Strategy for partitioning messages
        """
        self.broker = Broker(partition_strategy_type=partition_strategy_type)
        
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
        return self.broker.create_topic(name, num_partitions, replication_factor)
    
    def delete_topic(self, name):
        """
        Delete a topic.
        
        Args:
            name (str): Topic name
            
        Returns:
            bool: True if topic was deleted, False if it doesn't exist
        """
        return self.broker.delete_topic(name)
    
    def get_topic(self, name):
        """
        Get a topic by name.
        
        Args:
            name (str): Topic name
            
        Returns:
            Topic: The topic, or None if not found
        """
        return self.broker.get_topic(name)
    
    def get_all_topics(self):
        """
        Get all topics.
        
        Returns:
            list: List of all topics
        """
        return self.broker.get_all_topics()
    
    def create_producer(self):
        """
        Create a new producer.
        
        Returns:
            Producer: The created producer
        """
        producer = Producer(broker=self.broker)
        self.broker.register_producer(producer)
        return producer
    
    def create_consumer(self, group_id=None):
        """
        Create a new consumer.
        
        Args:
            group_id (str, optional): Consumer group ID
            
        Returns:
            Consumer: The created consumer
        """
        consumer = Consumer(group_id=group_id, broker=self.broker)
        self.broker.register_consumer(consumer)
        return consumer
    
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
        return self.broker.send_message(topic_name, value, key, producer_id)
    
    def get_topic_messages(self, topic_name):
        """
        Get all messages for a topic.
        
        Args:
            topic_name (str): Topic name
            
        Returns:
            list: List of all messages in the topic
        """
        topic = self.broker.get_topic(topic_name)
        if not topic:
            return []
        
        messages = []
        for partition in topic.get_all_partitions():
            messages.extend(partition.messages)
        
        return messages

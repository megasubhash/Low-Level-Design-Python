from services.MessageBrokerService import MessageBrokerService
from enums.PartitionStrategy import PartitionStrategy
import time

def print_topic_info(topic):
    """Print topic information."""
    print(f"Topic: {topic.name}")
    print(f"Partitions: {topic.num_partitions}")
    print(f"Replication Factor: {topic.replication_factor}")
    
    total_messages = 0
    for partition_id, partition in topic.partitions.items():
        print(f"  Partition {partition_id}: {len(partition.messages)} messages")
        total_messages += len(partition.messages)
    
    print(f"Total Messages: {total_messages}")
    print("-" * 50)

def test_round_robin_partitioning():
    """Test round-robin partition strategy."""
    print("\n=== Testing Round Robin Partitioning ===")
    
    # Create service with round-robin partitioning
    service = MessageBrokerService(partition_strategy_type=PartitionStrategy.ROUND_ROBIN)
    
    # Create a topic with multiple partitions
    service.create_topic("test-topic", num_partitions=3)
    
    # Create a producer
    producer = service.create_producer()
    
    # Send messages to the topic
    for i in range(10):
        message_id = producer.send("test-topic", f"Message {i}")
        print(f"Sent message {i} with ID: {message_id}")
    
    # Get the topic and print information
    topic = service.get_topic("test-topic")
    print_topic_info(topic)
    
    # Verify round-robin distribution
    print("Message distribution (should be even across partitions):")
    for partition_id, partition in topic.partitions.items():
        print(f"  Partition {partition_id}: {len(partition.messages)} messages")
    
    return service

def test_key_based_partitioning():
    """Test key-based partition strategy."""
    print("\n=== Testing Key-Based Partitioning ===")
    
    # Create service with key-based partitioning
    service = MessageBrokerService(partition_strategy_type=PartitionStrategy.KEY_BASED)
    
    # Create a topic with multiple partitions
    service.create_topic("orders", num_partitions=3)
    
    # Create a producer
    producer = service.create_producer()
    
    # Send messages with different keys
    keys = ["user1", "user2", "user3", "user1", "user2", "user3"]
    for i, key in enumerate(keys):
        message_id = producer.send("orders", f"Order {i} for {key}", key=key)
        print(f"Sent order {i} for {key} with ID: {message_id}")
    
    # Get the topic and print information
    topic = service.get_topic("orders")
    print_topic_info(topic)
    
    # Verify that messages with the same key went to the same partition
    print("Messages by key:")
    for key in set(keys):
        print(f"  Messages for key '{key}':")
        for partition_id, partition in topic.partitions.items():
            key_messages = [m for m in partition.messages if m.key == key]
            if key_messages:
                print(f"    Partition {partition_id}: {len(key_messages)} messages")
    
    return service

def test_consumer_groups():
    """Test consumer groups."""
    print("\n=== Testing Consumer Groups ===")
    
    # Create service
    service = MessageBrokerService()
    
    # Create a topic with multiple partitions
    service.create_topic("events", num_partitions=4)
    
    # Create a producer
    producer = service.create_producer()
    
    # Send messages to the topic
    for i in range(20):
        producer.send("events", f"Event {i}")
    
    # Create consumers in the same group
    group_id = "event-processors"
    consumers = []
    for i in range(2):
        consumer = service.create_consumer(group_id=group_id)
        consumer.subscribe("events")
        consumers.append(consumer)
        print(f"Created consumer {i} in group '{group_id}'")
    
    # Poll for messages
    print("\nPolling for messages:")
    for i, consumer in enumerate(consumers):
        messages = consumer.poll(max_messages=5)
        print(f"Consumer {i} received {len(messages)} messages:")
        for msg in messages:
            print(f"  {msg.value} (Partition: {msg.partition}, Offset: {msg.offset})")
    
    # Poll again to get more messages
    print("\nPolling again:")
    for i, consumer in enumerate(consumers):
        messages = consumer.poll(max_messages=5)
        print(f"Consumer {i} received {len(messages)} messages:")
        for msg in messages:
            print(f"  {msg.value} (Partition: {msg.partition}, Offset: {msg.offset})")
    
    return service, consumers

def test_multiple_topics():
    """Test multiple topics."""
    print("\n=== Testing Multiple Topics ===")
    
    # Create service
    service = MessageBrokerService()
    
    # Create multiple topics
    topics = ["clicks", "views", "purchases"]
    for topic_name in topics:
        service.create_topic(topic_name, num_partitions=2)
        print(f"Created topic: {topic_name}")
    
    # Create producers for each topic
    producers = {}
    for topic_name in topics:
        producer = service.create_producer()
        producers[topic_name] = producer
        print(f"Created producer for topic: {topic_name}")
    
    # Send messages to each topic
    for topic_name, producer in producers.items():
        for i in range(5):
            producer.send(topic_name, f"{topic_name.capitalize()} event {i}")
        print(f"Sent 5 messages to topic: {topic_name}")
    
    # Create a consumer that subscribes to all topics
    consumer = service.create_consumer()
    for topic_name in topics:
        consumer.subscribe(topic_name)
    print(f"Consumer subscribed to {len(topics)} topics")
    
    # Poll for messages from all topics
    print("\nPolling for messages from all topics:")
    messages = consumer.poll(max_messages=15)
    
    # Group messages by topic
    messages_by_topic = {}
    for msg in messages:
        if msg.topic not in messages_by_topic:
            messages_by_topic[msg.topic] = []
        messages_by_topic[msg.topic].append(msg)
    
    # Print messages by topic
    for topic_name, topic_messages in messages_by_topic.items():
        print(f"Messages from topic '{topic_name}': {len(topic_messages)}")
        for msg in topic_messages:
            print(f"  {msg.value}")
    
    return service, consumer

def main():
    print("Kafka-like Pub-Sub Messaging System Demo")
    print("=======================================\n")
    
    # Run test cases
    test_round_robin_partitioning()
    test_key_based_partitioning()
    test_consumer_groups()
    test_multiple_topics()

if __name__ == "__main__":
    main()

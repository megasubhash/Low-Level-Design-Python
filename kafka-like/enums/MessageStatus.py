from enum import Enum

class MessageStatus(Enum):
    """Enum for message statuses."""
    PENDING = "PENDING"       # Message is pending delivery
    DELIVERED = "DELIVERED"   # Message has been delivered to broker
    CONSUMED = "CONSUMED"     # Message has been consumed by consumer
    FAILED = "FAILED"         # Message delivery failed

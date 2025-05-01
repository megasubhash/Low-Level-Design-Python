from enum import Enum

class PackageStatus(Enum):
    PENDING = "PENDING"  # Package is registered but not yet delivered to locker
    DELIVERED = "DELIVERED"  # Package is delivered to locker
    PICKED_UP = "PICKED_UP"  # Package has been picked up by customer
    RETURNED = "RETURNED"  # Package was not picked up and has been returned
    EXPIRED = "EXPIRED"  # Package pickup time has expired

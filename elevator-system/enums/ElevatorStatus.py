from enum import Enum

class ElevatorStatus(Enum):
    IDLE = "IDLE"
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    MAINTENANCE = "MAINTENANCE"

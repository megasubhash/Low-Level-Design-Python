functions

user should select floor from inside

user should be able to select the direction on the floor

Admin can add/remove lift


<!-- entities -->
Floor
Elevator
Building
User
ElevatorStatus
Direction

user -> Elevator -> Floor -> Building

class Elevator
    - id: str
    - current_floor: int
    - status: ElevatorStatus
    - direction: 
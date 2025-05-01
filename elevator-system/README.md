# Elevator System

A flexible and extensible elevator system implementation with support for different scheduling strategies.

## Features

- **Multiple Elevator Scheduling Strategies**:
  - Shortest Path Strategy: Minimizes passenger wait time by selecting the closest elevator
  - Least Busy Strategy: Distributes load evenly among elevators by selecting the least busy one
  - Energy Efficient Strategy: Minimizes energy consumption by optimizing elevator movements

- **Clean Architecture**:
  - Models: Core data structures (Elevator, Building, ElevatorRequest)
  - Interfaces: Contracts for implementations
  - Strategies: Different elevator scheduling algorithms
  - Factory: Creates appropriate scheduling strategies
  - Services: Business logic for elevator operations

- **Elevator Management**:
  - Create and manage buildings with multiple floors
  - Add elevators to buildings
  - Create internal and external elevator requests
  - Track elevator status and movement
  - Simulate elevator system behavior

## Project Structure

```
elevator-system/
├── models/
│   ├── Elevator.py
│   ├── Building.py
│   ├── ElevatorRequest.py
│   └── ElevatorManager.py
├── interfaces/
│   └── IElevatorSchedulingStrategy.py
├── strategies/
│   ├── ShortestPathSchedulingStrategy.py
│   ├── LeastBusySchedulingStrategy.py
│   └── EnergyEfficientSchedulingStrategy.py
├── factory/
│   └── ElevatorSchedulingStrategyFactory.py
├── services/
│   └── ElevatorService.py
├── enums/
│   ├── Direction.py
│   ├── ElevatorStatus.py
│   └── RequestStatus.py
└── main.py
```

## Usage

### Command Line Interface

```bash
# Building Management
python main.py building add "Office Tower" --floors 20 --basements 2
python main.py building list
python main.py building show <building_id>

# Elevator Management
python main.py elevator add <building_id> --floor 0 --capacity 10
python main.py elevator add-multiple <building_id> 5
python main.py elevator list <building_id>
python main.py elevator show <building_id> <elevator_id>

# Request Management
python main.py request external <building_id> 5 UP
python main.py request internal <building_id> <elevator_id> 10

# Simulation
python main.py simulate <building_id> --steps 20 --delay 0.5
```

### Programmatic Usage

```python
from models.ElevatorManager import ElevatorManager
from services.ElevatorService import ElevatorService
from enums.Direction import Direction

# Create components
service = ElevatorService(scheduling_strategy_type="shortest_path")
manager = ElevatorManager(service)

# Add a building
building_id = manager.add_building("Office Tower", 20, 2)

# Add elevators to the building
for _ in range(5):
    manager.add_elevator(building_id)

# Create an external request (from a floor button)
request_id = manager.create_external_request(building_id, 5, Direction.UP)

# Run the simulation
for _ in range(10):
    status_updates = manager.step_simulation()
    print(status_updates)
```

## Elevator Scheduling Strategies

### Shortest Path Strategy
This strategy selects the elevator that would reach the request floor in the shortest time. It considers:
- Current distance between elevator and request floor
- Elevator direction and current destinations
- Penalties for direction changes

### Least Busy Strategy
This strategy selects the elevator with the fewest destination floors. It aims to distribute load evenly among elevators and prevent any single elevator from becoming overloaded.

### Energy Efficient Strategy
This strategy selects the elevator that would consume the least energy to serve the request. It considers:
- Distance to travel
- Direction changes (which consume more energy)
- Current elevator load
- Continuous movement vs. start/stop cycles

## Requirements

- Python 3.6+

## Installation

1. Clone the repository
2. No external dependencies required

## License

MIT

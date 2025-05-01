# Amazon Locker System

A flexible and extensible Amazon Locker system implementation with support for different locker allocation strategies.

## Features

- **Multiple Locker Allocation Strategies**:
  - Best Fit Strategy: Allocates the smallest suitable locker for a package
  - First Fit Strategy: Allocates the first available suitable locker
  - Random Strategy: Allocates a random suitable locker

- **Clean Architecture**:
  - Models: Core data structures (Locker, Package, LockerLocation)
  - Interfaces: Contracts for implementations
  - Strategies: Different locker allocation algorithms
  - Factory: Creates appropriate allocation strategies
  - Services: Business logic for locker operations
  - Repository: Stores locker, package, and location information

- **Locker Management**:
  - Create and manage locker locations
  - Add lockers of different sizes
  - Register packages for delivery
  - Assign lockers to packages
  - Deliver packages to lockers
  - Pick up packages with verification
  - Track package status and expiry

## Project Structure

```
amazon-locker/
├── models/
│   ├── Locker.py
│   ├── Package.py
│   ├── LockerLocation.py
│   └── LockerManager.py
├── interfaces/
│   └── ILockerAllocationStrategy.py
├── strategies/
│   ├── BestFitLockerAllocationStrategy.py
│   ├── FirstFitLockerAllocationStrategy.py
│   └── RandomLockerAllocationStrategy.py
├── factory/
│   └── LockerAllocationStrategyFactory.py
├── services/
│   └── LockerService.py
├── repository/
│   └── LockerRepository.py
├── enums/
│   ├── LockerSize.py
│   ├── LockerStatus.py
│   └── PackageStatus.py
└── main.py
```

## Usage

### Command Line Interface

```bash
# Location Management
python main.py location add "Downtown Hub" "123 Main St" "Seattle" "WA" "98101"
python main.py location list
python main.py location show <location_id>

# Locker Management
python main.py locker add <location_id> --size MEDIUM
python main.py locker add-multiple <location_id> 10 --small 3 --medium 4 --large 2 --extra-large 1

# Package Management
python main.py package register <user_id> --size MEDIUM --description "Electronics"
python main.py package assign <package_id> <location_id>
python main.py package deliver <package_id>
python main.py package pickup <package_id> <pickup_code>
python main.py package list
python main.py package list --status DELIVERED
python main.py package list --user <user_id>
python main.py package show <package_id>
python main.py package check-expired
```

### Programmatic Usage

```python
from models.LockerManager import LockerManager
from services.LockerService import LockerService
from repository.LockerRepository import LockerRepository
from enums.LockerSize import LockerSize

# Create components
repo = LockerRepository()
service = LockerService(repo, allocation_strategy_type="best_fit")
manager = LockerManager(service)

# Add a location
location_id = manager.add_location("Downtown Hub", "123 Main St", "Seattle", "WA", "98101")

# Add lockers to the location
for _ in range(5):
    manager.add_locker(location_id, LockerSize.MEDIUM)

# Register a package
package_id = manager.register_package("user123", LockerSize.MEDIUM, "Electronics")

# Assign a locker to the package
locker_id = manager.assign_locker(package_id, location_id)

# Deliver the package
manager.deliver_package(package_id)

# Pick up the package
package = manager.get_package(package_id)
manager.pickup_package(package_id, package.pickup_code)
```

## Requirements

- Python 3.6+

## Installation

1. Clone the repository
2. No external dependencies required

## License

MIT

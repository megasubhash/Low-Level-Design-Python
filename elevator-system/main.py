import time
from models.ElevatorManager import ElevatorManager
from services.ElevatorService import ElevatorService
from enums.Direction import Direction
from enums.ElevatorStatus import ElevatorStatus
from enums.RequestStatus import RequestStatus

def display_elevator_status(elevator):
    """Display detailed elevator information."""
    print(f"Elevator ID: {elevator['id']}")
    print(f"Current Floor: {elevator['floor']}")
    print(f"Status: {elevator['status']}")
    print(f"Direction: {elevator['direction']}")
    print(f"Destinations: {elevator['destinations']}")
    print(f"Capacity: {elevator['capacity']}")
    print(f"Current Load: {elevator['current_capacity']}")

def display_building_info(building):
    """Display detailed building information."""
    print(f"Building ID: {building.id}")
    print(f"Name: {building.name}")
    print(f"Floors: {building.num_floors} (above ground)")
    print(f"Basements: {building.num_basements}")
    print(f"Total Elevators: {len(building.elevators)}")
    
    # Count elevators by status
    status_counts = {}
    for elevator in building.elevators.values():
        status_counts[elevator.status.value] = status_counts.get(elevator.status.value, 0) + 1
    
    print(f"Elevators by Status: {status_counts}")

def run_simulation(manager, building_id, steps=10, delay=0.5):
    """Run the elevator simulation for a specified number of steps."""
    building = manager.get_building(building_id)
    if not building:
        print(f"Building not found: {building_id}")
        return
    
    print(f"Running simulation for building: {building.name}")
    print(f"Total steps: {steps}")
    print(f"Delay between steps: {delay} seconds")
    print("-" * 50)
    
    for step in range(1, steps + 1):
        print(f"\nStep {step}:")
        
        # Step the simulation
        status_updates = manager.step_simulation()
        
        if building_id in status_updates:
            elevator_updates = status_updates[building_id]
            
            for elevator_id, update in elevator_updates.items():
                print(f"Elevator {elevator_id[:8]}: Floor {update['floor']}, {update['status']}, {update['direction']}, Destinations: {update['destinations']}")
        
        # Wait before next step
        if step < steps:
            time.sleep(delay)
    
    print("\nSimulation complete!")

def test_shortest_path_strategy():
    """Test case for the ShortestPathSchedulingStrategy."""
    print("\n=== Testing Shortest Path Strategy ===")
    service = ElevatorService(scheduling_strategy_type="shortest_path")
    manager = ElevatorManager(service)
    
    # Create a building with 20 floors
    building_id = manager.add_building("Office Tower", 20, 2)
    print(f"Created building with ID: {building_id}")
    
    # Add 3 elevators to the building
    elevator_ids = []
    for i in range(3):
        elevator_id = manager.add_elevator(building_id, i*5, 10)  # Start at different floors
        elevator_ids.append(elevator_id)
        print(f"Added elevator {i+1} with ID: {elevator_id}")
    
    # Create external requests
    request1 = manager.create_external_request(building_id, 15, Direction.DOWN)
    request2 = manager.create_external_request(building_id, 3, Direction.UP)
    request3 = manager.create_external_request(building_id, 18, Direction.DOWN)
    
    print(f"Created external requests: {request1}, {request2}, {request3}")
    
    # Run simulation
    run_simulation(manager, building_id, 15, 0.2)

def test_least_busy_strategy():
    """Test case for the LeastBusySchedulingStrategy."""
    print("\n=== Testing Least Busy Strategy ===")
    service = ElevatorService(scheduling_strategy_type="least_busy")
    manager = ElevatorManager(service)
    
    # Create a building with 15 floors
    building_id = manager.add_building("Shopping Mall", 15, 1)
    print(f"Created building with ID: {building_id}")
    
    # Add 4 elevators to the building
    elevator_ids = []
    for i in range(4):
        elevator_id = manager.add_elevator(building_id, 0, 15)  # All start at ground floor
        elevator_ids.append(elevator_id)
        print(f"Added elevator {i+1} with ID: {elevator_id}")
    
    # Add some initial destinations to make elevators busy
    manager.create_internal_request(building_id, elevator_ids[0], 10)
    manager.create_internal_request(building_id, elevator_ids[0], 12)
    manager.create_internal_request(building_id, elevator_ids[1], 5)
    manager.create_internal_request(building_id, elevator_ids[1], 8)
    manager.create_internal_request(building_id, elevator_ids[1], 11)
    
    # Create new external requests - should go to least busy elevators
    request1 = manager.create_external_request(building_id, 7, Direction.UP)
    request2 = manager.create_external_request(building_id, 14, Direction.DOWN)
    
    print(f"Created external requests: {request1}, {request2}")
    
    # Run simulation
    run_simulation(manager, building_id, 20, 0.2)

def test_energy_efficient_strategy():
    """Test case for the EnergyEfficientSchedulingStrategy."""
    print("\n=== Testing Energy Efficient Strategy ===")
    service = ElevatorService(scheduling_strategy_type="energy_efficient")
    manager = ElevatorManager(service)
    
    # Create a building with 30 floors
    building_id = manager.add_building("Residential Tower", 30, 3)
    print(f"Created building with ID: {building_id}")
    
    # Add 5 elevators to the building at different floors
    elevator_ids = []
    for i in range(5):
        elevator_id = manager.add_elevator(building_id, i*6, 8)  # Different starting positions
        elevator_ids.append(elevator_id)
        print(f"Added elevator {i+1} with ID: {elevator_id}")
    
    # Create a mix of internal and external requests
    manager.create_internal_request(building_id, elevator_ids[0], 25)
    manager.create_internal_request(building_id, elevator_ids[1], 15)
    manager.create_internal_request(building_id, elevator_ids[2], 10)
    
    request1 = manager.create_external_request(building_id, 22, Direction.DOWN)
    request2 = manager.create_external_request(building_id, 8, Direction.UP)
    request3 = manager.create_external_request(building_id, 28, Direction.DOWN)
    
    print(f"Created external requests: {request1}, {request2}, {request3}")
    
    # Run simulation
    run_simulation(manager, building_id, 25, 0.2)

def test_mixed_scenarios():
    """Test case with mixed scenarios and multiple buildings."""
    print("\n=== Testing Mixed Scenarios ===")
    service = ElevatorService(scheduling_strategy_type="shortest_path")
    manager = ElevatorManager(service)
    
    # Create multiple buildings
    building1_id = manager.add_building("Office Tower", 20, 2)
    building2_id = manager.add_building("Hotel", 25, 1)
    
    # Add elevators to buildings
    for i in range(3):
        manager.add_elevator(building1_id, 0, 10)
    
    for i in range(4):
        manager.add_elevator(building2_id, 0, 12)
    
    # Create requests for both buildings
    manager.create_external_request(building1_id, 15, Direction.DOWN)
    manager.create_external_request(building1_id, 3, Direction.UP)
    
    manager.create_external_request(building2_id, 20, Direction.DOWN)
    manager.create_external_request(building2_id, 5, Direction.UP)
    manager.create_external_request(building2_id, 12, Direction.DOWN)
    
    # Run simulation for first building
    print("\nSimulating first building:")
    run_simulation(manager, building1_id, 10, 0.2)
    
    # Run simulation for second building
    print("\nSimulating second building:")
    run_simulation(manager, building2_id, 10, 0.2)

def main():
    print("Elevator System Test Cases")
    print("==========================\n")
    
    # Run test cases
    test_shortest_path_strategy()
    test_least_busy_strategy()
    test_energy_efficient_strategy()
    test_mixed_scenarios()

if __name__ == "__main__":
    main()

from models.ParkingLot import ParkingLot
from models.ParkingFloor import ParkingFloor
from models.ParkingSpot import ParkingSpotFactory, HandicappedSpot, CompactSpot, LargeSpot, MotorcycleSpot, ElectricSpot
from models.Vehicle import Car, ElectricVehicle, Motorcycle, Van, Truck, VehicleFactory
from enums.ParkingSpotType import ParkingSpotType
from enums.VehicleType import VehicleType
from enums.SpotAllocationStrategy import SpotAllocationStrategy
from services.ParkingLotService import ParkingLotService
from strategies.HourlyPricingStrategy import HourlyPricingStrategy
from factory.PricingStrategyFactory import PricingStrategyFactory, PricingStrategyType

def setup_parking_lot():
    """Set up a sample parking lot."""
    # Create parking lot using Singleton pattern
    parking_lot = ParkingLot("Downtown Parking", "123 Main St", 50)
    
    # Create floors
    floor1 = ParkingFloor(1, 20)
    floor2 = ParkingFloor(2, 30)
    
    # Add spots to floor 1 using ParkingSpotFactory
    for i in range(1, 11):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.COMPACT, i)
        floor1.add_spot(spot)
    
    for i in range(11, 16):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.LARGE, i)
        floor1.add_spot(spot)
    
    for i in range(16, 21):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.MOTORCYCLE, i)
        floor1.add_spot(spot)
    
    # Add spots to floor 2 using ParkingSpotFactory
    for i in range(1, 16):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.COMPACT, i)
        floor2.add_spot(spot)
    
    for i in range(16, 26):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.LARGE, i)
        floor2.add_spot(spot)
    
    for i in range(26, 31):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.ELECTRIC, i)
        floor2.add_spot(spot)
        
    # Add a few handicapped spots to floor 1
    for i in range(31, 34):
        spot = ParkingSpotFactory.create_spot(ParkingSpotType.HANDICAPPED, i)
        floor1.add_spot(spot)
    
    # Add floors to parking lot
    parking_lot.add_floor(floor1)
    parking_lot.add_floor(floor2)
    
    return parking_lot

def demo_parking_lot():
    """Demonstrate parking lot operations."""
    print("Parking Lot System Demo")
    print("======================\n")
    
    # Set up parking lot - using Singleton pattern
    parking_lot = setup_parking_lot()
    
    # Create service - using Singleton pattern
    service = ParkingLotService(parking_lot, SpotAllocationStrategy.NEAREST)
    
    # Demonstrate Singleton pattern
    print("Demonstrating Singleton Pattern:")
    second_parking_lot = ParkingLot("Another Parking Lot", "456 Side St", 200)
    print(f"First parking lot name: {parking_lot.name}")
    print(f"Second parking lot name: {second_parking_lot.name}")
    print(f"Are they the same object? {parking_lot is second_parking_lot}")
    print("-" * 50)
    
    # Create pricing strategy using factory
    pricing_strategy = PricingStrategyFactory.create_strategy(PricingStrategyType.HOURLY)
    
    # Print initial status
    status = service.get_parking_lot_status()
    print(f"Parking lot: {status['name']}")
    print(f"Total capacity: {status['total_capacity']}")
    print(f"Available capacity: {status['available_capacity']}")
    print(f"Occupancy: {status['occupancy_percentage']:.2f}%\n")
    
    # Park vehicles using the Vehicle hierarchy
    print("Parking vehicles using Vehicle hierarchy...")
    
    # Using vehicle types for compatibility with existing service
    vehicles_to_park = [
        ("ABC123", VehicleType.CAR),
        ("DEF456", VehicleType.CAR),
        ("GHI789", VehicleType.ELECTRIC),
        ("JKL012", VehicleType.MOTORCYCLE),
        ("MNO345", VehicleType.VAN)
    ]
    
    tickets = []
    for license_plate, vehicle_type in vehicles_to_park:
        ticket = service.park_vehicle(license_plate, vehicle_type)
        if ticket:
            tickets.append(ticket)
            print(f"Parked {vehicle_type.value} with license plate {license_plate}")
            print(f"Ticket ID: {ticket.id}")
            print(f"Issued at: {ticket.issued_at}")
            print("-" * 50)
    
    # Print updated status
    status = service.get_parking_lot_status()
    print(f"\nUpdated parking lot status:")
    print(f"Available capacity: {status['available_capacity']}")
    print(f"Occupancy: {status['occupancy_percentage']:.2f}%\n")
    
    # Unpark a vehicle
    if tickets:
        print("Unparking a vehicle...")
        ticket = tickets[0]
        success, fee = service.unpark_vehicle(ticket.id, pricing_strategy)
        
        if success:
            print(f"Vehicle unparked successfully")
            print(f"Parking fee: ${fee:.2f}")
        else:
            print("Failed to unpark vehicle")
    
    # Print final status
    status = service.get_parking_lot_status()
    print(f"\nFinal parking lot status:")
    print(f"Available capacity: {status['available_capacity']}")
    print(f"Occupancy: {status['occupancy_percentage']:.2f}%")

if __name__ == "__main__":
    demo_parking_lot()

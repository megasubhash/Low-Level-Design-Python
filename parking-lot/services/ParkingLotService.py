from datetime import datetime
from models.Vehicle import VehicleFactory
from models.ParkingTicket import ParkingTicket
from enums.ParkingTicketStatus import ParkingTicketStatus
from enums.SpotAllocationStrategy import SpotAllocationStrategy
from factory.SpotAllocationStrategyFactory import SpotAllocationStrategyFactory

class ParkingLotService:
    """Service for parking lot operations. Implements the Singleton pattern."""
    
    _instance = None
    
    def __new__(cls, parking_lot=None, allocation_strategy=SpotAllocationStrategy.NEAREST):
        """Create a new instance of ParkingLotService or return the existing one."""
        if cls._instance is None:
            cls._instance = super(ParkingLotService, cls).__new__(cls)
            cls._instance.parking_lot = parking_lot
            cls._instance.allocation_strategy = allocation_strategy
            cls._instance.vehicles = {}  # Map of vehicle_id to Vehicle
            cls._instance.tickets = {}  # Map of ticket_id to ParkingTicket
        return cls._instance
    
    def __init__(self, parking_lot=None, allocation_strategy=SpotAllocationStrategy.NEAREST):
        """Initialize the ParkingLotService (only used for the first instance)."""
        # The initialization is done in __new__, so this method is empty
        pass
    
    def park_vehicle(self, license_plate, vehicle_type):
        """
        Park a vehicle.
        
        Args:
            license_plate (str): License plate of the vehicle
            vehicle_type (VehicleType): Type of the vehicle
            
        Returns:
            ParkingTicket: Issued parking ticket, or None if parking failed
        """
        # Create or retrieve vehicle
        vehicle = None
        for v in self.vehicles.values():
            if v.license_plate == license_plate:
                vehicle = v
                break
        
        if not vehicle:
            # Use the VehicleFactory to create the appropriate vehicle type
            vehicle = VehicleFactory.create_vehicle(vehicle_type, license_plate)
            self.vehicles[vehicle.id] = vehicle
        
        # Allocate a spot
        strategy = SpotAllocationStrategyFactory.create_strategy(self.allocation_strategy)
        spot = strategy.allocate_spot(self.parking_lot, vehicle.get_vehicle_type())
        
        if not spot:
            return None  # No available spot
        
        # Assign vehicle to spot
        spot.assign_vehicle(vehicle.id)
        
        # Create and return ticket
        ticket = ParkingTicket(vehicle.id, spot.id)
        self.tickets[ticket.id] = ticket
        
        return ticket
    
    def unpark_vehicle(self, ticket_id, pricing_strategy):
        """
        Unpark a vehicle.
        
        Args:
            ticket_id (str): ID of the parking ticket
            pricing_strategy (IPricingStrategy): Strategy for pricing
            
        Returns:
            tuple: (success, amount) where success is a boolean and amount is the fee
        """
        ticket = self.tickets.get(ticket_id)
        if not ticket or ticket.status != ParkingTicketStatus.ACTIVE:
            return False, 0
        
        # Find the spot
        spot = None
        for floor in self.parking_lot.floors.values():
            if ticket.spot_id in floor.spots:
                spot = floor.spots[ticket.spot_id]
                break
        
        if not spot:
            return False, 0
        
        # Calculate fee
        fee = pricing_strategy.calculate_price(ticket, spot.get_spot_type())
        
        # Update ticket
        ticket.mark_as_paid(fee)
        
        # Free the spot
        spot.remove_vehicle()
        
        return True, fee
    
    def get_parking_lot_status(self):
        """
        Get the status of the parking lot.
        
        Returns:
            dict: Status information
        """
        total_spots = sum(len(floor.spots) for floor in self.parking_lot.floors.values())
        occupied_spots = sum(
            len([spot for spot in floor.spots.values() if spot.is_occupied])
            for floor in self.parking_lot.floors.values()
        )
        
        return {
            "name": self.parking_lot.name,
            "total_capacity": total_spots,
            "available_capacity": total_spots - occupied_spots,
            "occupancy_percentage": (occupied_spots / total_spots * 100) if total_spots > 0 else 0
        }

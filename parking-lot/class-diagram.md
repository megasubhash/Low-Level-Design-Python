classDiagram
    ParkingSpot
    ParkingFloor
    ParkingLot
    Vehicle (Car, Bike, Truck)
    ParkingSpotType
    Ticket
    ParkingSpotStatus
    ParkingLotManager
    TicketStatus
    

class ParkingSpot
    - id: str
    - spot_type: ParkingSpotType
    - vehicle: Vehicle
    - status: ParkingSpotStatus
    - ticket: Ticket
    - park_vehicle() -> Ticket
    - un_park_vehicle() -> Ticket

class ParkingFloor
    - id : str
    - spots: Map<id: ParkingSpot>
    - add_spot() -> bool
    - remove_spot() -> bool

class ParkingLot
    - id
    - name
    - address
    - floors: Map<floor_id: ParkingFloor>
    - add_floor() -> bool
    - remove_floor() -> bool

class Vehicle
    - vehicle_number: str
    - spot: Spot
    - ticket: Ticket
    - parked_timestamp: timestamp

enum VehicleType
    - CAR, BIKE, TAXI, TRUCK

class Car<Vehicle>
    - vehicle_type: VehicleType

class Ticket
    - id
    - created_at: timestamp
    - vehicle: Vehicle
    - parked_at: timestamp
    - spot: ParkingSpot
    - status: TicketStatus
    - amount: float
    - calculate_bill() -> float


class ParkingLotManager
    - parking_lot: ParkingLot
    - get_status -> Map<str, Map>
    - park_vehicle() -> Ticket
    - un_park_vehicle() -> Ticket
    - get_nearest_spot -> Spot
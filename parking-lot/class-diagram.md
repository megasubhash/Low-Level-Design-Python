```mermaid
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

    class PricingStrategyFactory {
        +get_strategy()
    }
    
    class ParkingLotService {
        +park_vehicle()
        +un_park_vehicle()
        +calculate_bill()
        +get_status()
    }
```

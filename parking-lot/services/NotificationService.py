from datetime import datetime

class NotificationService:
    """Service for sending notifications related to parking lot operations."""
    
    def __init__(self):
        """Initialize the NotificationService."""
        self.notifications = []  # Store notifications for demo purposes
    
    def send_ticket_notification(self, ticket, vehicle_license_plate):
        """
        Send a notification about a parking ticket.
        
        Args:
            ticket (ParkingTicket): The parking ticket
            vehicle_license_plate (str): License plate of the vehicle
            
        Returns:
            bool: True if notification was sent successfully
        """
        message = f"Parking ticket issued for vehicle {vehicle_license_plate} at {ticket.issued_at}. Ticket ID: {ticket.id}"
        self.notifications.append({
            "type": "TICKET_ISSUED",
            "message": message,
            "timestamp": datetime.now()
        })
        
        # In a real implementation, this would send an SMS, email, or push notification
        print(f"NOTIFICATION: {message}")
        return True
    
    def send_payment_notification(self, ticket, amount, vehicle_license_plate):
        """
        Send a notification about a payment.
        
        Args:
            ticket (ParkingTicket): The parking ticket
            amount (float): Amount paid
            vehicle_license_plate (str): License plate of the vehicle
            
        Returns:
            bool: True if notification was sent successfully
        """
        message = f"Payment of ${amount:.2f} received for vehicle {vehicle_license_plate}. Ticket ID: {ticket.id}"
        self.notifications.append({
            "type": "PAYMENT_RECEIVED",
            "message": message,
            "timestamp": datetime.now()
        })
        
        # In a real implementation, this would send an SMS, email, or push notification
        print(f"NOTIFICATION: {message}")
        return True
    
    def send_capacity_alert(self, parking_lot_name, available_capacity, threshold=10):
        """
        Send an alert when parking lot capacity falls below a threshold.
        
        Args:
            parking_lot_name (str): Name of the parking lot
            available_capacity (int): Available capacity
            threshold (int): Threshold for sending alert
            
        Returns:
            bool: True if alert was sent successfully
        """
        if available_capacity <= threshold:
            message = f"ALERT: Parking lot {parking_lot_name} is nearly full! Only {available_capacity} spots remaining."
            self.notifications.append({
                "type": "CAPACITY_ALERT",
                "message": message,
                "timestamp": datetime.now()
            })
            
            # In a real implementation, this would send an SMS, email, or push notification
            print(f"NOTIFICATION: {message}")
            return True
        
        return False
    
    def get_recent_notifications(self, count=10):
        """
        Get recent notifications.
        
        Args:
            count (int): Number of notifications to retrieve
            
        Returns:
            list: List of recent notifications
        """
        return sorted(self.notifications, key=lambda n: n["timestamp"], reverse=True)[:count]

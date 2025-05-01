import os
import argparse
from datetime import datetime
from models.LockerManager import LockerManager
from services.LockerService import LockerService
from repository.LockerRepository import LockerRepository
from enums.LockerSize import LockerSize
from enums.LockerStatus import LockerStatus
from enums.PackageStatus import PackageStatus

def display_package_info(package):
    """Display detailed package information."""
    print(f"Package ID: {package.id}")
    print(f"Status: {package.status.value}")
    print(f"Size: {package.size.value}")
    print(f"Description: {package.description or 'N/A'}")
    print(f"User ID: {package.user_id}")
    print(f"Pickup Code: {package.pickup_code}")
    
    if package.locker_id:
        print(f"Locker ID: {package.locker_id}")
        print(f"Location ID: {package.location_id}")
    
    print(f"Created: {package.created_at}")
    
    if package.delivered_at:
        print(f"Delivered: {package.delivered_at}")
    
    if package.picked_up_at:
        print(f"Picked up: {package.picked_up_at}")
    
    if package.expiry_date:
        print(f"Expires: {package.expiry_date}")
        if package.is_expired():
            print("Status: EXPIRED")

def display_location_info(location):
    """Display detailed location information."""
    print(f"Location ID: {location.id}")
    print(f"Name: {location.name}")
    print(f"Address: {location.address}")
    print(f"City: {location.city}, {location.state} {location.zip_code}")
    print(f"Active: {'Yes' if location.is_active else 'No'}")
    
    # Count lockers by size and status
    size_counts = {}
    status_counts = {}
    
    for locker in location.lockers.values():
        size_counts[locker.size.value] = size_counts.get(locker.size.value, 0) + 1
        status_counts[locker.status.value] = status_counts.get(locker.status.value, 0) + 1
    
    print(f"Total Lockers: {len(location.lockers)}")
    print(f"Lockers by Size: {size_counts}")
    print(f"Lockers by Status: {status_counts}")

def main():
    parser = argparse.ArgumentParser(description="Amazon Locker System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Location commands
    location_parser = subparsers.add_parser("location", help="Location management")
    location_subparsers = location_parser.add_subparsers(dest="location_command")
    
    # Add location
    add_location_parser = location_subparsers.add_parser("add", help="Add a new location")
    add_location_parser.add_argument("name", help="Location name")
    add_location_parser.add_argument("address", help="Street address")
    add_location_parser.add_argument("city", help="City")
    add_location_parser.add_argument("state", help="State")
    add_location_parser.add_argument("zip_code", help="ZIP code")
    
    # List locations
    list_locations_parser = location_subparsers.add_parser("list", help="List all locations")
    
    # Show location details
    show_location_parser = location_subparsers.add_parser("show", help="Show location details")
    show_location_parser.add_argument("location_id", help="Location ID")
    
    # Locker commands
    locker_parser = subparsers.add_parser("locker", help="Locker management")
    locker_subparsers = locker_parser.add_subparsers(dest="locker_command")
    
    # Add locker
    add_locker_parser = locker_subparsers.add_parser("add", help="Add a new locker")
    add_locker_parser.add_argument("location_id", help="Location ID")
    add_locker_parser.add_argument("--size", choices=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"], default="MEDIUM", help="Locker size")
    
    # Add multiple lockers
    add_multiple_lockers_parser = locker_subparsers.add_parser("add-multiple", help="Add multiple lockers")
    add_multiple_lockers_parser.add_argument("location_id", help="Location ID")
    add_multiple_lockers_parser.add_argument("count", type=int, help="Number of lockers to add")
    add_multiple_lockers_parser.add_argument("--small", type=int, default=0, help="Number of small lockers")
    add_multiple_lockers_parser.add_argument("--medium", type=int, default=0, help="Number of medium lockers")
    add_multiple_lockers_parser.add_argument("--large", type=int, default=0, help="Number of large lockers")
    add_multiple_lockers_parser.add_argument("--extra-large", type=int, default=0, help="Number of extra large lockers")
    
    # Package commands
    package_parser = subparsers.add_parser("package", help="Package management")
    package_subparsers = package_parser.add_subparsers(dest="package_command")
    
    # Register package
    register_package_parser = package_subparsers.add_parser("register", help="Register a new package")
    register_package_parser.add_argument("user_id", help="User ID")
    register_package_parser.add_argument("--size", choices=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"], default="MEDIUM", help="Package size")
    register_package_parser.add_argument("--description", help="Package description")
    
    # Assign locker
    assign_locker_parser = package_subparsers.add_parser("assign", help="Assign a locker to a package")
    assign_locker_parser.add_argument("package_id", help="Package ID")
    assign_locker_parser.add_argument("location_id", help="Location ID")
    
    # Deliver package
    deliver_package_parser = package_subparsers.add_parser("deliver", help="Mark a package as delivered")
    deliver_package_parser.add_argument("package_id", help="Package ID")
    deliver_package_parser.add_argument("--access-code", help="Custom access code (optional)")
    
    # Pickup package
    pickup_package_parser = package_subparsers.add_parser("pickup", help="Pick up a package")
    pickup_package_parser.add_argument("package_id", help="Package ID")
    pickup_package_parser.add_argument("pickup_code", help="Pickup code")
    
    # List packages
    list_packages_parser = package_subparsers.add_parser("list", help="List all packages")
    list_packages_parser.add_argument("--status", choices=["PENDING", "DELIVERED", "PICKED_UP", "RETURNED", "EXPIRED"], help="Filter by status")
    list_packages_parser.add_argument("--user", help="Filter by user ID")
    
    # Show package details
    show_package_parser = package_subparsers.add_parser("show", help="Show package details")
    show_package_parser.add_argument("package_id", help="Package ID")
    
    # Check expired packages
    check_expired_parser = package_subparsers.add_parser("check-expired", help="Check for expired packages")
    
    args = parser.parse_args()
    
    # Create components
    repo = LockerRepository()
    service = LockerService(repo)
    manager = LockerManager(service)
    
    # Load existing locations
    for location in service.get_all_locations():
        manager.locations[location.id] = location
    
    # Load existing packages
    for package in service.get_all_packages():
        manager.packages[package.id] = package
        manager.packages_by_status[package.status.value].append(package.id)
        if package.user_id:
            manager.packages_by_user[package.user_id].append(package.id)
    
    # Handle commands
    if args.command == "location":
        if args.location_command == "add":
            # Add a new location
            location_id = manager.add_location(
                args.name,
                args.address,
                args.city,
                args.state,
                args.zip_code
            )
            print(f"Location added with ID: {location_id}")
        
        elif args.location_command == "list":
            # List all locations
            locations = manager.get_all_locations()
            if not locations:
                print("No locations found.")
            else:
                print("ID | Name | Address | Lockers")
                print("-" * 80)
                for location in locations:
                    print(f"{location.id[:8]} | {location.name} | {location.address}, {location.city} | {len(location.lockers)}")
                print(f"Total: {len(locations)} locations")
        
        elif args.location_command == "show":
            # Show location details
            location = manager.get_location(args.location_id)
            if location:
                display_location_info(location)
            else:
                print(f"Location not found: {args.location_id}")
    
    elif args.command == "locker":
        if args.locker_command == "add":
            # Add a new locker
            locker_size = LockerSize(args.size)
            locker_id = manager.add_locker(args.location_id, locker_size)
            
            if locker_id:
                print(f"Locker added with ID: {locker_id}")
            else:
                print(f"Failed to add locker to location: {args.location_id}")
        
        elif args.locker_command == "add-multiple":
            # Add multiple lockers
            location = manager.get_location(args.location_id)
            if not location:
                print(f"Location not found: {args.location_id}")
                return
            
            total_added = 0
            
            # Add small lockers
            for _ in range(args.small):
                locker_id = manager.add_locker(args.location_id, LockerSize.SMALL)
                if locker_id:
                    total_added += 1
            
            # Add medium lockers
            for _ in range(args.medium):
                locker_id = manager.add_locker(args.location_id, LockerSize.MEDIUM)
                if locker_id:
                    total_added += 1
            
            # Add large lockers
            for _ in range(args.large):
                locker_id = manager.add_locker(args.location_id, LockerSize.LARGE)
                if locker_id:
                    total_added += 1
            
            # Add extra large lockers
            for _ in range(args.extra_large):
                locker_id = manager.add_locker(args.location_id, LockerSize.EXTRA_LARGE)
                if locker_id:
                    total_added += 1
            
            # If specific sizes weren't provided, add the requested count as medium
            remaining = args.count - total_added
            for _ in range(remaining):
                locker_id = manager.add_locker(args.location_id, LockerSize.MEDIUM)
                if locker_id:
                    total_added += 1
            
            print(f"Added {total_added} lockers to location: {args.location_id}")
    
    elif args.command == "package":
        if args.package_command == "register":
            # Register a new package
            package_size = LockerSize(args.size)
            package_id = manager.register_package(
                args.user_id,
                package_size,
                args.description
            )
            
            package = manager.get_package(package_id)
            print(f"Package registered with ID: {package_id}")
            print(f"Pickup Code: {package.pickup_code}")
        
        elif args.package_command == "assign":
            # Assign a locker to a package
            locker_id = manager.assign_locker(args.package_id, args.location_id)
            
            if locker_id:
                package = manager.get_package(args.package_id)
                print(f"Package {args.package_id} assigned to locker {locker_id} at location {args.location_id}")
            else:
                print(f"Failed to assign locker for package {args.package_id} at location {args.location_id}")
        
        elif args.package_command == "deliver":
            # Deliver a package
            result = manager.deliver_package(args.package_id, args.access_code)
            
            if result:
                package = manager.get_package(args.package_id)
                locker = service.get_locker(package.locker_id)
                print(f"Package {args.package_id} delivered to locker {package.locker_id}")
                print(f"Access Code: {locker.access_code}")
                print(f"Expires: {package.expiry_date}")
            else:
                print(f"Failed to deliver package {args.package_id}")
        
        elif args.package_command == "pickup":
            # Pick up a package
            result = manager.pickup_package(args.package_id, args.pickup_code)
            
            if result:
                print(f"Package {args.package_id} picked up successfully")
            else:
                print(f"Failed to pick up package {args.package_id}. Invalid pickup code or package not available.")
        
        elif args.package_command == "list":
            # List packages
            packages = []
            
            if args.status:
                status = PackageStatus(args.status)
                packages = manager.get_packages_by_status(status)
            elif args.user:
                packages = manager.get_packages_by_user(args.user)
            else:
                packages = list(manager.packages.values())
            
            if not packages:
                print("No packages found.")
            else:
                print("ID | Status | Size | User | Location | Locker")
                print("-" * 80)
                for package in packages:
                    location_id = package.location_id or "N/A"
                    locker_id = package.locker_id or "N/A"
                    print(f"{package.id[:8]} | {package.status.value} | {package.size.value} | {package.user_id} | {location_id[:8] if location_id != 'N/A' else 'N/A'} | {locker_id[:8] if locker_id != 'N/A' else 'N/A'}")
                print(f"Total: {len(packages)} packages")
        
        elif args.package_command == "show":
            # Show package details
            package = manager.get_package(args.package_id)
            if package:
                display_package_info(package)
            else:
                print(f"Package not found: {args.package_id}")
        
        elif args.package_command == "check-expired":
            # Check for expired packages
            expired_package_ids = service.check_expired_packages()
            
            if expired_package_ids:
                print(f"Found {len(expired_package_ids)} expired packages:")
                for package_id in expired_package_ids:
                    package = manager.get_package(package_id)
                    print(f"  {package_id[:8]} - Expired on {package.expiry_date}")
            else:
                print("No expired packages found.")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

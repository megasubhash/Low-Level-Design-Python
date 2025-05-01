import os
import time
import argparse
from models.S3Manager import S3Manager
from services.S3Service import S3Service
from repository.S3OperationRepository import S3OperationRepository
from enums.S3OperationType import S3OperationType
from enums.S3OperationStatus import S3OperationStatus

def display_progress(operation):
    """Display operation progress in the console."""
    if operation.status == S3OperationStatus.IN_PROGRESS:
        progress_bar = "=" * int(operation.progress / 2) + ">" + " " * (50 - int(operation.progress / 2))
        print(f"\r[{progress_bar}] {operation.progress:.1f}% - {operation.operation_type.value} - {operation.object_key}", end="")
    else:
        print(f"\r{operation.status.value} - {operation.operation_type.value} - {operation.object_key} - {operation.progress:.1f}%")

def main():
    parser = argparse.ArgumentParser(description="AWS S3 Manager CLI")
    parser.add_argument("--profile", help="AWS profile name to use")
    parser.add_argument("--region", help="AWS region name")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file to S3")
    upload_parser.add_argument("local_path", help="Local file path")
    upload_parser.add_argument("bucket", help="S3 bucket name")
    upload_parser.add_argument("key", help="S3 object key")
    upload_parser.add_argument("--multipart", action="store_true", help="Use multipart upload")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download a file from S3")
    download_parser.add_argument("bucket", help="S3 bucket name")
    download_parser.add_argument("key", help="S3 object key")
    download_parser.add_argument("local_path", help="Local file path")
    download_parser.add_argument("--multipart", action="store_true", help="Use multipart download")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an object from S3")
    delete_parser.add_argument("bucket", help="S3 bucket name")
    delete_parser.add_argument("key", help="S3 object key")
    
    # Copy command
    copy_parser = subparsers.add_parser("copy", help="Copy an object in S3")
    copy_parser.add_argument("source_bucket", help="Source bucket name")
    copy_parser.add_argument("source_key", help="Source object key")
    copy_parser.add_argument("dest_bucket", help="Destination bucket name")
    copy_parser.add_argument("dest_key", help="Destination object key")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List objects in a bucket")
    list_parser.add_argument("bucket", help="S3 bucket name")
    list_parser.add_argument("--prefix", help="Prefix to filter objects")
    
    # List operations command
    list_ops_parser = subparsers.add_parser("list-ops", help="List all operations")
    
    args = parser.parse_args()
    
    # Get AWS credentials from environment or profile
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region_name = args.region or os.environ.get('AWS_REGION')
    
    # Create components
    repo = S3OperationRepository()
    service = S3Service(repo, aws_access_key, aws_secret_key, region_name)
    manager = S3Manager(service)
    
    if args.command == "upload":
        # Create and start upload operation
        operation_id = manager.upload_file(args.local_path, args.bucket, args.key)
        print(f"Upload operation created with ID: {operation_id}")
        
        # Start operation with appropriate strategy
        strategy_type = "multipart" if args.multipart else "standard"
        result = service.start_operation(operation_id, strategy_type)
        
        if result:
            print(f"Started uploading {args.local_path} to s3://{args.bucket}/{args.key}")
            
            # Monitor progress
            while True:
                operation = manager.get_operation(operation_id)
                if not operation:
                    print("\nOperation not found.")
                    break
                
                display_progress(operation)
                
                if operation.status in [S3OperationStatus.COMPLETED, S3OperationStatus.FAILED, S3OperationStatus.CANCELLED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to start upload operation.")
    
    elif args.command == "download":
        # Create and start download operation
        operation_id = manager.download_file(args.bucket, args.key, args.local_path)
        print(f"Download operation created with ID: {operation_id}")
        
        # Start operation with appropriate strategy
        strategy_type = "multipart" if args.multipart else "standard"
        result = service.start_operation(operation_id, strategy_type)
        
        if result:
            print(f"Started downloading s3://{args.bucket}/{args.key} to {args.local_path}")
            
            # Monitor progress
            while True:
                operation = manager.get_operation(operation_id)
                if not operation:
                    print("\nOperation not found.")
                    break
                
                display_progress(operation)
                
                if operation.status in [S3OperationStatus.COMPLETED, S3OperationStatus.FAILED, S3OperationStatus.CANCELLED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to start download operation.")
    
    elif args.command == "delete":
        # Create and start delete operation
        operation_id = manager.delete_object(args.bucket, args.key)
        print(f"Delete operation created with ID: {operation_id}")
        
        # Start operation
        result = service.start_operation(operation_id)
        
        if result:
            print(f"Started deleting s3://{args.bucket}/{args.key}")
            
            # Monitor progress
            while True:
                operation = manager.get_operation(operation_id)
                if not operation:
                    print("\nOperation not found.")
                    break
                
                display_progress(operation)
                
                if operation.status in [S3OperationStatus.COMPLETED, S3OperationStatus.FAILED, S3OperationStatus.CANCELLED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to start delete operation.")
    
    elif args.command == "copy":
        # Create and start copy operation
        operation_id = manager.copy_object(args.source_bucket, args.source_key, args.dest_bucket, args.dest_key)
        print(f"Copy operation created with ID: {operation_id}")
        
        # Start operation
        result = service.start_operation(operation_id)
        
        if result:
            print(f"Started copying s3://{args.source_bucket}/{args.source_key} to s3://{args.dest_bucket}/{args.dest_key}")
            
            # Monitor progress
            while True:
                operation = manager.get_operation(operation_id)
                if not operation:
                    print("\nOperation not found.")
                    break
                
                display_progress(operation)
                
                if operation.status in [S3OperationStatus.COMPLETED, S3OperationStatus.FAILED, S3OperationStatus.CANCELLED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to start copy operation.")
    
    elif args.command == "list":
        # List objects in bucket
        objects = manager.list_objects(args.bucket, args.prefix)
        
        if objects:
            print(f"Objects in s3://{args.bucket}/{args.prefix or ''}:")
            for obj in objects:
                print(f"  {obj}")
            print(f"Total: {len(objects)} objects")
        else:
            print(f"No objects found in s3://{args.bucket}/{args.prefix or ''}")
    
    elif args.command == "list-ops":
        # List all operations
        operations = manager.get_all_operations()
        
        if operations:
            print("ID | Type | Status | Progress | Bucket | Key")
            print("-" * 80)
            for op in operations:
                print(f"{op.id[:8]} | {op.operation_type.value} | {op.status.value} | {op.progress:.1f}% | {op.bucket_name} | {op.object_key}")
            print(f"Total: {len(operations)} operations")
        else:
            print("No operations found.")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

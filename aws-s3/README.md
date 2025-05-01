# AWS S3 Manager

A flexible and extensible AWS S3 operations manager with support for different S3 operation strategies.

## Features

- **Multiple S3 Strategies**:
  - Standard S3 Strategy: Basic S3 operations
  - Multipart S3 Strategy: Optimized for large files with multipart upload/download

- **Supported Operations**:
  - Upload: Upload files to S3 buckets
  - Download: Download files from S3 buckets
  - Delete: Delete objects from S3 buckets
  - Copy: Copy objects between S3 buckets or within the same bucket
  - List: List objects in S3 buckets

- **Clean Architecture**:
  - Models: Core data structures
  - Interfaces: Contracts for implementations
  - Strategies: Different S3 operation algorithms
  - Factory: Creates appropriate S3 strategies
  - Services: Business logic for S3 operations
  - Repository: Stores operation information

- **Operation Management**:
  - Create, start, and cancel operations
  - Track operation progress
  - Persistent storage of operation information

## Project Structure

```
aws-s3/
├── models/
│   ├── S3Operation.py
│   └── S3Manager.py
├── interfaces/
│   └── IS3Strategy.py
├── strategies/
│   ├── StandardS3Strategy.py
│   └── MultipartS3Strategy.py
├── factory/
│   └── S3StrategyFactory.py
├── services/
│   └── S3Service.py
├── repository/
│   └── S3OperationRepository.py
├── enums/
│   ├── S3OperationType.py
│   └── S3OperationStatus.py
└── main.py
```

## Usage

### Command Line Interface

```bash
# Upload a file to S3
python main.py upload local_file.txt my-bucket my-key

# Upload a large file using multipart upload
python main.py upload large_file.zip my-bucket my-key --multipart

# Download a file from S3
python main.py download my-bucket my-key local_file.txt

# Download a large file using multipart download
python main.py download my-bucket my-key large_file.zip --multipart

# Delete an object from S3
python main.py delete my-bucket my-key

# Copy an object in S3
python main.py copy source-bucket source-key dest-bucket dest-key

# List objects in a bucket
python main.py list my-bucket

# List objects with a prefix
python main.py list my-bucket --prefix folder/

# List all operations
python main.py list-ops
```

### Programmatic Usage

```python
from models.S3Manager import S3Manager
from services.S3Service import S3Service
from repository.S3OperationRepository import S3OperationRepository

# Create components
repo = S3OperationRepository()
service = S3Service(repo, aws_access_key, aws_secret_key, region_name)
manager = S3Manager(service)

# Upload a file
operation_id = manager.upload_file("local_file.txt", "my-bucket", "my-key")
service.start_operation(operation_id, "multipart")  # Use multipart for large files

# Download a file
operation_id = manager.download_file("my-bucket", "my-key", "local_file.txt")
service.start_operation(operation_id)

# Delete an object
operation_id = manager.delete_object("my-bucket", "my-key")
service.start_operation(operation_id)

# Copy an object
operation_id = manager.copy_object("source-bucket", "source-key", "dest-bucket", "dest-key")
service.start_operation(operation_id)

# List objects
objects = manager.list_objects("my-bucket", "prefix/")
```

## Requirements

- Python 3.6+
- boto3

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install boto3
   ```
3. Configure AWS credentials:
   - Set environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
   - Or use AWS CLI profiles

## License

MIT

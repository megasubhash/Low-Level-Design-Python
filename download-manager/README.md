# Download Manager

A flexible and extensible download manager implementation with support for different download strategies.

## Features

- **Multiple Download Strategies**:
  - Simple Download: Basic download functionality
  - Parallel Download: Downloads files in parallel chunks for faster downloads
  - Resumable Download: Supports pausing and resuming downloads

- **Clean Architecture**:
  - Models: Core data structures
  - Interfaces: Contracts for implementations
  - Strategies: Different download algorithms
  - Factory: Creates appropriate download strategies
  - Services: Business logic for download operations
  - Repository: Stores download information

- **Download Management**:
  - Add, start, pause, resume, and cancel downloads
  - Track download progress
  - Persistent storage of download information

## Project Structure

```
download-manager/
├── models/
│   ├── Download.py
│   └── DownloadManager.py
├── interfaces/
│   └── IDownloadStrategy.py
├── strategies/
│   ├── SimpleDownloadStrategy.py
│   ├── ParallelDownloadStrategy.py
│   └── ResumeDownloadStrategy.py
├── factory/
│   └── DownloadStrategyFactory.py
├── services/
│   └── DownloadService.py
├── repository/
│   └── DownloadRepository.py
├── enums/
│   ├── DownloadStatus.py
│   └── DownloadType.py
└── main.py
```

## Usage

### Command Line Interface

```bash
# Start a new download
python main.py https://example.com/file.zip -d downloads -t simple

# List all downloads
python main.py -l

# Pause a download
python main.py -p <download_id>

# Resume a download
python main.py -r <download_id>

# Cancel a download
python main.py -c <download_id>
```

### Programmatic Usage

```python
from models.DownloadManager import DownloadManager
from services.DownloadService import DownloadService
from repository.DownloadRepository import DownloadRepository
from enums.DownloadType import DownloadType

# Create components
repo = DownloadRepository()
service = DownloadService(repo)
manager = DownloadManager(service)

# Add a download
download_id = manager.add_download(
    url="https://example.com/file.zip",
    destination_path="downloads",
    download_type=DownloadType.PARALLEL
)

# Start the download
manager.start_download(download_id)

# Get download progress
download = manager.get_download(download_id)
print(f"Progress: {download.progress}%")

# Pause, resume, cancel
manager.pause_download(download_id)
manager.resume_download(download_id)
manager.cancel_download(download_id)
```

## Requirements

- Python 3.6+
- requests

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install requests
   ```

## License

MIT

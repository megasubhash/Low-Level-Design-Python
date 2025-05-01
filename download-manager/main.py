import os
import time
import argparse
from models.Download import Download
from enums.DownloadType import DownloadType
from enums.DownloadStatus import DownloadStatus
from repository.DownloadRepository import DownloadRepository
from services.DownloadService import DownloadService
from factory.DownloadStrategyFactory import DownloadStrategyFactory
from models.DownloadManager import DownloadManager

def display_progress(download):
    """Display download progress in the console."""
    if download.status == DownloadStatus.DOWNLOADING:
        progress_bar = "=" * int(download.progress / 2) + ">" + " " * (50 - int(download.progress / 2))
        print(f"\r[{progress_bar}] {download.progress:.1f}% - {download.file_name}", end="")
    else:
        print(f"\r{download.status.value} - {download.file_name} - {download.progress:.1f}%")

def main():
    parser = argparse.ArgumentParser(description="Download Manager CLI")
    parser.add_argument("url", nargs="?", help="URL to download")
    parser.add_argument("-d", "--destination", help="Destination directory", default="downloads")
    parser.add_argument("-t", "--type", choices=["simple", "parallel", "resumable"], 
                        default="simple", help="Download type")
    parser.add_argument("-l", "--list", action="store_true", help="List all downloads")
    parser.add_argument("-p", "--pause", help="Pause download by ID")
    parser.add_argument("-r", "--resume", help="Resume download by ID")
    parser.add_argument("-c", "--cancel", help="Cancel download by ID")
    
    args = parser.parse_args()
    
    # Create download repository
    download_repo = DownloadRepository()
    
    # Create download service
    download_service = DownloadService(download_repo)
    
    # Create download manager
    download_manager = DownloadManager(download_service)
    
    # Handle commands
    if args.list:
        # List all downloads
        downloads = download_manager.get_all_downloads()
        if not downloads:
            print("No downloads found.")
        else:
            print("ID | Status | Progress | URL | File Name")
            print("-" * 80)
            for download in downloads:
                print(f"{download.id[:8]} | {download.status.value} | {download.progress:.1f}% | {download.url} | {download.file_name}")
    
    elif args.pause:
        # Pause download
        result = download_manager.pause_download(args.pause)
        if result:
            print(f"Download {args.pause} paused successfully.")
        else:
            print(f"Failed to pause download {args.pause}.")
    
    elif args.resume:
        # Resume download
        result = download_manager.resume_download(args.resume)
        if result:
            print(f"Download {args.resume} resumed successfully.")
            
            # Monitor progress
            while True:
                download = download_manager.get_download(args.resume)
                if not download:
                    print("\nDownload not found.")
                    break
                
                display_progress(download)
                
                if download.status in [DownloadStatus.COMPLETED, DownloadStatus.FAILED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to resume download {args.resume}.")
    
    elif args.cancel:
        # Cancel download
        result = download_manager.cancel_download(args.cancel)
        if result:
            print(f"Download {args.cancel} cancelled successfully.")
        else:
            print(f"Failed to cancel download {args.cancel}.")
    
    elif args.url:
        # Start a new download
        # Determine download type
        download_type = DownloadType.SIMPLE
        if args.type == "parallel":
            download_type = DownloadType.PARALLEL
        elif args.type == "resumable":
            download_type = DownloadType.RESUMABLE
        
        # Create destination directory if it doesn't exist
        os.makedirs(args.destination, exist_ok=True)
        
        # Add download
        download_id = download_manager.add_download(args.url, args.destination, download_type=download_type)
        print(f"Download added with ID: {download_id}")
        
        # Start download
        result = download_manager.start_download(download_id)
        if result:
            print(f"Download started: {args.url}")
            
            # Monitor progress
            while True:
                download = download_manager.get_download(download_id)
                if not download:
                    print("\nDownload not found.")
                    break
                
                display_progress(download)
                
                if download.status in [DownloadStatus.COMPLETED, DownloadStatus.FAILED]:
                    print()  # New line after completion
                    break
                
                time.sleep(0.5)
        else:
            print(f"Failed to start download: {args.url}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

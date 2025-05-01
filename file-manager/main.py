# Using placeholders instead of actual OS operations
from services.FileManagerService import FileManagerService
from enums.FilePermission import FilePermission
from enums.FileType import FileType
from enums.SortStrategy import SortStrategy
from enums.SearchStrategy import SearchStrategy

def print_file_info(file):
    """Print information about a file."""
    print(f"File: {file.name} (ID: {file.id})")
    print(f"Type: {file.file_type.value}")
    print(f"Size: {file.size} bytes")
    print(f"Created: {file.created_at}")
    print(f"Modified: {file.modified_at}")
    
    if file.tags:
        print(f"Tags: {', '.join(file.tags)}")
    
    print("-" * 50)

def print_directory_info(directory):
    """Print information about a directory."""
    print(f"Directory: {directory.name} (ID: {directory.id})")
    print(f"Files: {len(directory.files)}")
    print(f"Subdirectories: {len(directory.subdirectories)}")
    print(f"Created: {directory.created_at}")
    print(f"Modified: {directory.modified_at}")
    
    if directory.tags:
        print(f"Tags: {', '.join(directory.tags)}")
    
    print("-" * 50)

def demo_basic_operations():
    """Demonstrate basic file and directory operations."""
    print("\n=== Basic Operations Demo ===")
    
    # Using a placeholder for the root directory
    temp_dir = "/placeholder/root/directory"
    print(f"Using placeholder directory: {temp_dir}")
    
    # Create file manager
    file_manager = FileManagerService(root_path=temp_dir)
    
    # Create a user
    user_id = file_manager.create_user("testuser", "test@example.com", "password")
    file_manager.login("testuser", "password")
    print(f"Created and logged in user: {file_manager.get_current_user().username}")
    
    # Create directories
    docs_dir_id = file_manager.create_directory("Documents")
    images_dir_id = file_manager.create_directory("Images")
    
    print("\nCreated directories:")
    for dir_id in [docs_dir_id, images_dir_id]:
        directory = file_manager._find_directory(dir_id)
        print_directory_info(directory)
    
    # Create files
    text_content = b"This is a sample text file."
    image_content = b"Pretend this is image data"
    
    text_file_id = file_manager.create_file("sample.txt", text_content, docs_dir_id)
    image_file_id = file_manager.create_file("sample.jpg", image_content, images_dir_id)
    
    print("\nCreated files:")
    for file_id in [text_file_id, image_file_id]:
        file = file_manager._find_file(file_id)
        print_file_info(file)
    
    # Read file content
    text_content_read = file_manager.read_file(text_file_id)
    print(f"\nRead text file content: {text_content_read.decode('utf-8')}")
    
    # Update file content
    new_content = b"This is updated content."
    file_manager.write_file(text_file_id, new_content)
    
    # Read updated content
    updated_content = file_manager.read_file(text_file_id)
    print(f"Updated text file content: {updated_content.decode('utf-8')}")
    
    # Rename file
    file_manager.rename_file(text_file_id, "renamed.txt")
    renamed_file = file_manager._find_file(text_file_id)
    print(f"\nRenamed file: {renamed_file.name}")
    
    # Create a subdirectory
    subdir_id = file_manager.create_directory("Subdirectory", docs_dir_id)
    
    # Move file to subdirectory
    file_manager.move_file(text_file_id, subdir_id)
    
    # List files in documents directory
    print("\nFiles in Documents directory:")
    files = file_manager.list_files(docs_dir_id)
    for file in files:
        print(f"- {file.name}")
    
    # List files in documents directory (recursive)
    print("\nFiles in Documents directory (recursive):")
    files = file_manager.list_files(docs_dir_id, recursive=True)
    for file in files:
        # Get directory name without OS module
        dir_name = file.path.split('/')[-1] if file.path else 'unknown'
        print(f"- {file.name} (in {dir_name})")
    
    # Placeholder for cleanup
    print(f"\nCleanup would remove directory: {temp_dir}")
    
    return file_manager

def demo_search_and_sort():
    """Demonstrate search and sort operations."""
    print("\n=== Search and Sort Demo ===")
    
    # Using a placeholder for the root directory
    temp_dir = "/placeholder/root/directory"
    print(f"Using placeholder directory: {temp_dir}")
    
    # Create file manager
    file_manager = FileManagerService(root_path=temp_dir)
    
    # Create a user
    user_id = file_manager.create_user("testuser", "test@example.com", "password")
    file_manager.login("testuser", "password")
    
    # Create a directory
    dir_id = file_manager.create_directory("Files")
    
    # Create files with different creation times
    # Create files with different timestamps (no actual sleep)
    file_manager.create_file("document1.txt", b"Document 1 content", dir_id)
    file_manager.create_file("document2.txt", b"Document 2 content", dir_id)
    file_manager.create_file("image1.jpg", b"Image 1 content", dir_id)
    file_manager.create_file("image2.jpg", b"Image 2 content", dir_id)
    
    # Manually set creation times to simulate time differences
    files = file_manager.list_files(dir_id)
    for i, file in enumerate(files):
        # Set creation times 1 minute apart
        file.created_at = file.created_at.replace(minute=file.created_at.minute + i)
    
    # Sort files by name (ascending)
    print("\nFiles sorted by name (ascending):")
    files = file_manager.list_files(dir_id, sort_strategy=SortStrategy.NAME_ASC)
    for file in files:
        print(f"- {file.name}")
    
    # Sort files by name (descending)
    print("\nFiles sorted by name (descending):")
    files = file_manager.list_files(dir_id, sort_strategy=SortStrategy.NAME_DESC)
    for file in files:
        print(f"- {file.name}")
    
    # Sort files by creation date (ascending)
    print("\nFiles sorted by creation date (ascending):")
    files = file_manager.list_files(dir_id, sort_strategy=SortStrategy.DATE_CREATED_ASC)
    for file in files:
        print(f"- {file.name} (Created: {file.created_at})")
    
    # Sort files by creation date (descending)
    print("\nFiles sorted by creation date (descending):")
    files = file_manager.list_files(dir_id, sort_strategy=SortStrategy.DATE_CREATED_DESC)
    for file in files:
        print(f"- {file.name} (Created: {file.created_at})")
    
    # Search files by name
    print("\nSearch files by name (query='document'):")
    files = file_manager.search_files("document", search_strategy=SearchStrategy.NAME, dir_id=dir_id)
    for file in files:
        print(f"- {file.name}")
    
    # Search files by content
    print("\nSearch files by content (query='content'):")
    files = file_manager.search_files("content", search_strategy=SearchStrategy.CONTENT, dir_id=dir_id)
    for file in files:
        print(f"- {file.name}")
    
    # Placeholder for cleanup
    print(f"\nCleanup would remove directory: {temp_dir}")
    
    return file_manager

def demo_tags_and_permissions():
    """Demonstrate tags and permissions."""
    print("\n=== Tags and Permissions Demo ===")
    
    # Create file manager (in-memory only)
    file_manager = FileManagerService()
    
    # Create users
    admin_id = file_manager.create_user("admin", "admin@example.com", "admin_pass")
    user_id = file_manager.create_user("user", "user@example.com", "user_pass")
    
    # Log in as admin
    file_manager.login("admin", "admin_pass")
    print(f"Logged in as: {file_manager.get_current_user().username}")
    
    # Create directories and files
    docs_dir_id = file_manager.create_directory("Documents")
    private_dir_id = file_manager.create_directory("Private")
    
    file1_id = file_manager.create_file("public.txt", b"Public document", docs_dir_id)
    file2_id = file_manager.create_file("private.txt", b"Private document", private_dir_id)
    
    # Add tags
    file_manager.add_tag_to_file(file1_id, "public")
    file_manager.add_tag_to_file(file1_id, "document")
    file_manager.add_tag_to_file(file2_id, "private")
    file_manager.add_tag_to_file(file2_id, "document")
    
    file_manager.add_tag_to_directory(docs_dir_id, "public")
    file_manager.add_tag_to_directory(private_dir_id, "private")
    
    # Search by tag
    print("\nSearch by tag 'document':")
    files, _ = file_manager.search_by_tag("document")
    for file in files:
        print(f"- {file.name}")
    
    print("\nSearch by tag 'private':")
    files, directories = file_manager.search_by_tag("private")
    print("Files:")
    for file in files:
        print(f"- {file.name}")
    print("Directories:")
    for directory in directories:
        print(f"- {directory.name}")
    
    # Grant permissions to user
    file_manager.grant_permission(docs_dir_id, user_id, FilePermission.READ)
    file_manager.grant_permission(file1_id, user_id, FilePermission.READ)
    
    # Log in as regular user
    file_manager.logout()
    file_manager.login("user", "user_pass")
    print(f"\nLogged in as: {file_manager.get_current_user().username}")
    
    # Try to access files
    print("\nTrying to access files as regular user:")
    
    # Should succeed (has permission)
    content = file_manager.read_file(file1_id)
    print(f"Reading public.txt: {'Success' if content else 'Failed'}")
    
    # Should fail (no permission)
    content = file_manager.read_file(file2_id)
    print(f"Reading private.txt: {'Success' if content else 'Failed'}")
    
    return file_manager

def main():
    print("File Manager System Demo")
    print("=======================\n")
    
    # Run demos
    demo_basic_operations()
    demo_search_and_sort()
    demo_tags_and_permissions()

if __name__ == "__main__":
    main()

from services.GitService import GitService
from models.Repository import Repository
from models.Branch import Branch
from models.Commit import Commit
from enums.CommandType import CommandType
from enums.FileStatus import FileStatus
from enums.MergeStrategy import MergeStrategy
from strategies.FastForwardMergeStrategy import FastForwardMergeStrategy
import os
import sys

def print_help():
    """Print help information for the Git-like system."""
    print("Git-like Version Control System")
    print("==============================")
    print("\nCommands:")
    print("  init [path]                 - Initialize a new repository")
    print("  add <file>                  - Add a file to the staging area")
    print("  commit <message>            - Create a new commit with staged changes")
    print("  status                      - Show the repository status")
    print("  log [branch]                - Show commit history for a branch")
    print("  checkout <branch>           - Switch to a branch")
    print("  branch <name>               - Create a new branch")
    print("  merge <source> [target]     - Merge source branch into target branch")
    print("  exit                        - Exit the program")
    print("\nExample:")
    print("  init .")
    print("  add file.txt")
    print("  commit \"Initial commit\"")
    print("  branch feature")
    print("  checkout feature")
    print("  add another-file.txt")
    print("  commit \"Add another file\"")
    print("  checkout main")
    print("  merge feature")

def format_status(status):
    """Format the repository status for display."""
    if "error" in status:
        return f"Error: {status['error']}"
        
    result = f"On branch {status['branch']}\n"
    
    if status['commit']:
        result += f"HEAD -> {status['commit']}\n"
    else:
        result += "No commits yet\n"
        
    if status['staged_files']:
        result += "\nChanges to be committed:\n"
        for file in status['staged_files']:
            result += f"  new file: {file}\n"
            
    # Group files by status
    untracked = []
    modified = []
    
    for file, status_value in status['file_statuses'].items():
        if status_value == "untracked" and file not in status['staged_files']:
            untracked.append(file)
        elif status_value == "modified" and file not in status['staged_files']:
            modified.append(file)
            
    if modified:
        result += "\nChanges not staged for commit:\n"
        for file in modified:
            result += f"  modified: {file}\n"
            
    if untracked:
        result += "\nUntracked files:\n"
        for file in untracked:
            result += f"  {file}\n"
            
    if not status['staged_files'] and not modified and not untracked:
        result += "\nNothing to commit, working tree clean"
        
    return result

def run_git_demo():
    """Run a demonstration of the Git-like system with predefined commands."""
    git_service = GitService.get_instance()
    
    print("Git-like Version Control System Demo")
    print("==================================")
    print("This is an automated demonstration of the Git-like system.")
    print()
    
    # Create a demo directory
    demo_dir = os.path.join(os.getcwd(), "demo-repo")
    os.makedirs(demo_dir, exist_ok=True)
    os.chdir(demo_dir)
    
    # Create some demo files
    with open(os.path.join(demo_dir, "file1.txt"), "w") as f:
        f.write("This is the first file.\n")
        
    with open(os.path.join(demo_dir, "file2.txt"), "w") as f:
        f.write("This is the second file.\n")
    
    # List of predefined commands to demonstrate
    demo_commands = [
        ("init .", "Initializing a new repository"),
        ("status", "Checking repository status"),
        ("add file1.txt", "Adding file1.txt to staging area"),
        ("status", "Checking status after adding file1.txt"),
        ("commit \"Initial commit with file1\"", "Creating the first commit"),
        ("log", "Viewing commit history"),
        ("add file2.txt", "Adding file2.txt to staging area"),
        ("commit \"Add file2.txt\"", "Creating another commit"),
        ("log", "Viewing updated commit history"),
        ("branch feature", "Creating a new feature branch"),
        ("checkout feature", "Switching to the feature branch"),
        ("status", "Checking status on feature branch"),
    ]
    
    # Execute each demo command
    for command_line, description in demo_commands:
        try:
            # Display command with description
            print("\n" + "-"*50)
            print(f"DEMO: {description}")
            
            # Get the current directory
            current_dir = os.getcwd()
            
            # Get the current branch if repository is initialized
            branch_name = ""
            try:
                if git_service.repository.initialized:
                    branch_name = f" ({git_service.get_current_branch()})"
            except:
                pass
                
            # Display the command
            print(f"\n{current_dir}{branch_name}> {command_line}")
            
            # Split the command line into command and arguments
            parts = command_line.split(maxsplit=1)
            command = parts[0].lower() if parts else ""
            args = parts[1] if len(parts) > 1 else ""
            
            # Process the command
            if command == "help" or command == "":
                print_help()
                
            elif command == "exit" or command == "quit":
                print("Exiting...")
                break
                    
            elif command == "init":
                path = args or "."
                success = git_service.init(path)
                if success:
                    print(f"Initialized empty Git repository in {os.path.abspath(path)}")
                else:
                    print("Failed to initialize repository")
                        
            elif command == "add":
                if not args:
                    print("Error: No file specified")
                    continue
                    
                success = git_service.add(args)
                if success:
                    print(f"Added '{args}' to staging area")
                else:
                    print(f"Failed to add '{args}'")
                        
            elif command == "commit":
                if not args:
                    print("Error: No commit message specified")
                    continue
                    
                # Get author information from environment or use default
                author = os.environ.get("GIT_AUTHOR_NAME", "User") + " <" + os.environ.get("GIT_AUTHOR_EMAIL", "user@example.com") + ">"
                
                result = git_service.commit(args, author)
                if result["success"]:
                    print(f"[{result['commit_id']}] {result['message']}")
                else:
                    print(result["message"])
                        
            elif command == "status":
                status = git_service.status()
                print(format_status(status))
                    
            elif command == "log":
                branch = args or None
                commits = git_service.log(branch)
                
                if not commits:
                    print("No commits yet" if not branch else f"No commits in branch '{branch}'")
                else:
                    print("\n".join(commits))
                        
            elif command == "checkout":
                if not args:
                    print("Error: No branch specified")
                    continue
                    
                result = git_service.checkout(args)
                print(result["message"])
                    
            elif command == "branch":
                if not args:
                    # List branches
                    branches = git_service.get_branches()
                    current = git_service.get_current_branch()
                    
                    for branch in branches:
                        prefix = "* " if branch == current else "  "
                        print(f"{prefix}{branch}")
                else:
                    # Create a new branch
                    result = git_service.create_branch(args)
                    print(result["message"])
                        
            elif command == "merge":
                if not args:
                    print("Error: No source branch specified")
                    continue
                    
                # Split args into source and target branches
                merge_args = args.split(maxsplit=1)
                source = merge_args[0]
                target = merge_args[1] if len(merge_args) > 1 else None
                
                result = git_service.merge(source, target)
                print(result["message"])
                
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for usage information")
                    
        except KeyboardInterrupt:
            print("\nOperation aborted")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    """Main function."""
    run_git_demo()

if __name__ == "__main__":
    main()

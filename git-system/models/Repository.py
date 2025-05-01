import os
import json
import shutil
from models.Branch import Branch
from models.Commit import Commit
from enums.FileStatus import FileStatus

class Repository:
    """Represents a Git repository."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the repository."""
        if cls._instance is None:
            cls._instance = Repository()
        return cls._instance
    
    def __init__(self):
        """Initialize a new repository."""
        # Ensure this is a singleton
        if Repository._instance is not None:
            raise Exception("Repository is a singleton class. Use get_instance() to get the instance.")
        
        self.path = None
        self.git_dir = None
        self.branches = {}
        self.commits = {}
        self.staged_files = {}  # Files staged for commit
        self.current_branch = None
        self.initialized = False
        
    def init(self, path):
        """
        Initialize a new repository at the given path.
        
        Args:
            path (str): Path to initialize the repository
            
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        if self.initialized:
            return False
            
        self.path = os.path.abspath(path)
        self.git_dir = os.path.join(self.path, ".git-system")
        
        # Create .git-system directory and subdirectories
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        os.makedirs(os.path.join(self.git_dir, "refs", "heads"), exist_ok=True)
        
        # Create main branch
        main_branch = Branch("main")
        self.branches["main"] = main_branch
        self.current_branch = "main"
        
        # Save repository state
        self._save_state()
        
        self.initialized = True
        return True
        
    def add(self, file_path):
        """
        Add a file to the staging area.
        
        Args:
            file_path (str): Path to the file to add
            
        Returns:
            bool: True if the file was added successfully, False otherwise
        """
        if not self.initialized:
            return False
            
        # Convert to absolute path
        abs_path = os.path.abspath(file_path)
        
        # Check if the file exists
        if not os.path.isfile(abs_path):
            return False
            
        # Read the file content
        with open(abs_path, 'r') as f:
            content = f.read()
            
        # Get the relative path to the repository
        rel_path = os.path.relpath(abs_path, self.path)
        
        # Add to staged files
        self.staged_files[rel_path] = content
        
        # Save repository state
        self._save_state()
        
        return True
        
    def commit(self, message, author):
        """
        Create a new commit with the staged changes.
        
        Args:
            message (str): Commit message
            author (str): Author of the commit
            
        Returns:
            Commit or None: The created commit, or None if no files were staged
        """
        if not self.initialized or not self.staged_files:
            return None
            
        # Get the current branch
        branch = self.branches[self.current_branch]
        
        # Create a new commit
        parent_id = branch.commit_id
        commit = Commit(message, author, parent_id)
        
        # Add staged files to the commit
        for file_path, content in self.staged_files.items():
            commit.add_change(file_path, content)
            
        # Save the commit
        self.commits[commit.id] = commit
        
        # Update the branch to point to the new commit
        branch.update_commit(commit.id)
        
        # Clear staged files
        self.staged_files = {}
        
        # Save repository state
        self._save_state()
        
        return commit
        
    def status(self):
        """
        Get the status of the repository.
        
        Returns:
            dict: Repository status information
        """
        if not self.initialized:
            return {"error": "Repository not initialized"}
            
        # Get the current branch
        branch = self.branches[self.current_branch]
        
        # Get the current commit
        current_commit = self.commits.get(branch.commit_id)
        
        # Get all files in the repository
        all_files = self._get_all_files()
        
        # Determine the status of each file
        file_statuses = {}
        
        for file_path in all_files:
            # Skip .git-system directory
            if file_path.startswith(".git-system"):
                continue
                
            # Check if the file is staged
            if file_path in self.staged_files:
                file_statuses[file_path] = FileStatus.STAGED
            # Check if the file is in the current commit
            elif current_commit and file_path in current_commit.get_changes():
                # Check if the file has been modified
                with open(os.path.join(self.path, file_path), 'r') as f:
                    content = f.read()
                    
                if content != current_commit.get_changes()[file_path]:
                    file_statuses[file_path] = FileStatus.MODIFIED
                else:
                    file_statuses[file_path] = FileStatus.COMMITTED
            # File is untracked
            else:
                file_statuses[file_path] = FileStatus.UNTRACKED
                
        return {
            "branch": self.current_branch,
            "commit": branch.commit_id,
            "staged_files": list(self.staged_files.keys()),
            "file_statuses": {path: status.value for path, status in file_statuses.items()}
        }
        
    def log(self, branch_name=None):
        """
        Get the commit history for a branch.
        
        Args:
            branch_name (str, optional): Name of the branch. If None, use the current branch.
            
        Returns:
            list: List of commits in the branch
        """
        if not self.initialized:
            return []
            
        # Use current branch if not specified
        branch_name = branch_name or self.current_branch
        
        # Check if the branch exists
        if branch_name not in self.branches:
            return []
            
        # Get the branch
        branch = self.branches[branch_name]
        
        # Get the commit history
        commit_history = []
        commit_id = branch.commit_id
        
        while commit_id:
            commit = self.commits.get(commit_id)
            if not commit:
                break
                
            commit_history.append(commit)
            commit_id = commit.parent_id
            
        return commit_history
        
    def checkout(self, branch_name):
        """
        Checkout a branch.
        
        Args:
            branch_name (str): Name of the branch to checkout
            
        Returns:
            bool: True if checkout was successful, False otherwise
        """
        if not self.initialized:
            return False
            
        # Check if the branch exists
        if branch_name not in self.branches:
            return False
            
        # Cannot checkout if there are staged changes
        if self.staged_files:
            return False
            
        # Set the current branch
        self.current_branch = branch_name
        
        # Get the branch
        branch = self.branches[branch_name]
        
        # Get the commit
        commit = self.commits.get(branch.commit_id)
        
        # If there's a commit, restore the files
        if commit:
            # Clear the working directory
            for file_path in self._get_all_files():
                # Skip .git-system directory
                if file_path.startswith(".git-system"):
                    continue
                    
                # Remove the file
                os.remove(os.path.join(self.path, file_path))
                
            # Restore files from the commit
            for file_path, content in commit.get_changes().items():
                # Create directories if needed
                os.makedirs(os.path.dirname(os.path.join(self.path, file_path)), exist_ok=True)
                
                # Write the file
                with open(os.path.join(self.path, file_path), 'w') as f:
                    f.write(content)
                    
        # Save repository state
        self._save_state()
        
        return True
        
    def create_branch(self, branch_name):
        """
        Create a new branch.
        
        Args:
            branch_name (str): Name of the new branch
            
        Returns:
            bool: True if the branch was created successfully, False otherwise
        """
        if not self.initialized:
            return False
            
        # Check if the branch already exists
        if branch_name in self.branches:
            return False
            
        # Get the current branch
        current_branch = self.branches[self.current_branch]
        
        # Create a new branch pointing to the same commit
        new_branch = Branch(branch_name, current_branch.commit_id)
        self.branches[branch_name] = new_branch
        
        # Save repository state
        self._save_state()
        
        return True
        
    def _get_all_files(self):
        """
        Get all files in the repository.
        
        Returns:
            list: List of file paths relative to the repository root
        """
        all_files = []
        
        for root, dirs, files in os.walk(self.path):
            # Skip .git-system directory
            if ".git-system" in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.path)
                all_files.append(rel_path)
                
        return all_files
        
    def _save_state(self):
        """Save the repository state to disk."""
        if not self.git_dir:
            return
            
        # Save branches
        branches_data = {name: {"name": branch.name, "commit_id": branch.commit_id} 
                         for name, branch in self.branches.items()}
        
        with open(os.path.join(self.git_dir, "branches.json"), 'w') as f:
            json.dump(branches_data, f)
            
        # Save commits
        commits_data = {commit.id: {"id": commit.id, "message": commit.message, 
                                   "author": commit.author, "parent_id": commit.parent_id,
                                   "timestamp": commit.timestamp, "changes": commit.changes}
                        for commit in self.commits.values()}
        
        with open(os.path.join(self.git_dir, "commits.json"), 'w') as f:
            json.dump(commits_data, f)
            
        # Save staged files
        with open(os.path.join(self.git_dir, "staged.json"), 'w') as f:
            json.dump(self.staged_files, f)
            
        # Save current branch
        with open(os.path.join(self.git_dir, "HEAD"), 'w') as f:
            f.write(self.current_branch)
            
    def _load_state(self):
        """Load the repository state from disk."""
        if not self.git_dir or not os.path.exists(self.git_dir):
            return
            
        # Load branches
        branches_path = os.path.join(self.git_dir, "branches.json")
        if os.path.exists(branches_path):
            with open(branches_path, 'r') as f:
                branches_data = json.load(f)
                
            self.branches = {name: Branch(data["name"], data["commit_id"]) 
                            for name, data in branches_data.items()}
                
        # Load commits
        commits_path = os.path.join(self.git_dir, "commits.json")
        if os.path.exists(commits_path):
            with open(commits_path, 'r') as f:
                commits_data = json.load(f)
                
            self.commits = {}
            for commit_id, data in commits_data.items():
                commit = Commit(data["message"], data["author"], data["parent_id"])
                commit.id = data["id"]
                commit.timestamp = data["timestamp"]
                commit.changes = data["changes"]
                self.commits[commit_id] = commit
                
        # Load staged files
        staged_path = os.path.join(self.git_dir, "staged.json")
        if os.path.exists(staged_path):
            with open(staged_path, 'r') as f:
                self.staged_files = json.load(f)
                
        # Load current branch
        head_path = os.path.join(self.git_dir, "HEAD")
        if os.path.exists(head_path):
            with open(head_path, 'r') as f:
                self.current_branch = f.read().strip()
                
        self.initialized = True

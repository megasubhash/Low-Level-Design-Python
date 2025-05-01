from models.Repository import Repository
from strategies.FastForwardMergeStrategy import FastForwardMergeStrategy
from enums.MergeStrategy import MergeStrategy

class GitService:
    """Service for managing Git operations."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the git service."""
        if cls._instance is None:
            cls._instance = GitService()
        return cls._instance
    
    def __init__(self):
        """Initialize the git service."""
        # Ensure this is a singleton
        if GitService._instance is not None:
            raise Exception("GitService is a singleton class. Use get_instance() to get the instance.")
        
        self.repository = Repository.get_instance()
        self.merge_strategy = FastForwardMergeStrategy()
        
    def init(self, path):
        """
        Initialize a new repository at the given path.
        
        Args:
            path (str): Path to initialize the repository
            
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        return self.repository.init(path)
        
    def add(self, file_path):
        """
        Add a file to the staging area.
        
        Args:
            file_path (str): Path to the file to add
            
        Returns:
            bool: True if the file was added successfully, False otherwise
        """
        return self.repository.add(file_path)
        
    def commit(self, message, author):
        """
        Create a new commit with the staged changes.
        
        Args:
            message (str): Commit message
            author (str): Author of the commit
            
        Returns:
            dict: Information about the commit
        """
        commit = self.repository.commit(message, author)
        if not commit:
            return {"success": False, "message": "No changes to commit"}
            
        return {"success": True, "commit_id": commit.id, "message": commit.message}
        
    def status(self):
        """
        Get the status of the repository.
        
        Returns:
            dict: Repository status information
        """
        return self.repository.status()
        
    def log(self, branch_name=None):
        """
        Get the commit history for a branch.
        
        Args:
            branch_name (str, optional): Name of the branch. If None, use the current branch.
            
        Returns:
            list: List of commits in the branch
        """
        commits = self.repository.log(branch_name)
        return [str(commit) for commit in commits]
        
    def checkout(self, branch_name):
        """
        Checkout a branch.
        
        Args:
            branch_name (str): Name of the branch to checkout
            
        Returns:
            dict: Information about the checkout operation
        """
        success = self.repository.checkout(branch_name)
        if not success:
            return {"success": False, "message": f"Failed to checkout branch '{branch_name}'"}
            
        return {"success": True, "message": f"Switched to branch '{branch_name}'"}
        
    def create_branch(self, branch_name):
        """
        Create a new branch.
        
        Args:
            branch_name (str): Name of the new branch
            
        Returns:
            dict: Information about the branch creation
        """
        success = self.repository.create_branch(branch_name)
        if not success:
            return {"success": False, "message": f"Failed to create branch '{branch_name}'"}
            
        return {"success": True, "message": f"Created branch '{branch_name}'"}
        
    def merge(self, source_branch, target_branch=None):
        """
        Merge source branch into target branch.
        
        Args:
            source_branch (str): Name of the source branch
            target_branch (str, optional): Name of the target branch. If None, use the current branch.
            
        Returns:
            dict: Result of the merge operation
        """
        # Use current branch if target not specified
        target_branch = target_branch or self.repository.current_branch
        
        # Perform the merge using the strategy
        return self.merge_strategy.merge(source_branch, target_branch, self.repository)
        
    def get_current_branch(self):
        """
        Get the name of the current branch.
        
        Returns:
            str: Name of the current branch
        """
        return self.repository.current_branch
        
    def get_branches(self):
        """
        Get all branches in the repository.
        
        Returns:
            list: List of branch names
        """
        return list(self.repository.branches.keys())

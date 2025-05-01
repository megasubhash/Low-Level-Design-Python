class Branch:
    """Represents a branch in the Git repository."""
    
    def __init__(self, name, commit_id=None):
        """
        Initialize a new branch.
        
        Args:
            name (str): Name of the branch
            commit_id (str, optional): ID of the commit this branch points to
        """
        self.name = name
        self.commit_id = commit_id
        
    def update_commit(self, commit_id):
        """
        Update the commit this branch points to.
        
        Args:
            commit_id (str): ID of the new commit
        """
        self.commit_id = commit_id
        
    def __str__(self):
        """Return a string representation of the branch."""
        return f"{self.name} -> {self.commit_id if self.commit_id else 'No commits yet'}"

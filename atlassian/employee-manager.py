'''

Imagine you are the team that maintains the Atlassian employee directory. 

At Atlassian - there are multiple groups, and each can have one or more groups. Every employee is part of a group.

You are tasked with designing a system that could find the closest common parent group  given a target set of employees in the organization. 

Assumptions : (We expect the candidate to ask these proactively, if not try and guide them towards these) 

a group node can have both employees and groups

We don't have employees shared across different groups 

We don't have repeats of the same Employee name ( i.e: node value) at this stage.

We dont have 2 isolated trees in the company ( i.e: everything rolls up to a single root) 

 As an extension to discussions, you can probe candidates on what they would do one or many of the assumptions where not present. ( the next level up removes the second assumption mentioned here )  

 Tie breaking:  

The Atlassian hierarchy sometimes can have shared group across an org or employees shared across different groups - How will the code evolve in this case if the requirement is to provide ONE closest common group? 

The system now introduced 4 methods to update the structure of the hierarchy in the org. Suppose these dynamic updates are done in separate threads while getCommonGroupForEmployees is being called, How will your system handled reads and writes into the system efficiently such that at any given time getCommonGroupForEmployees always reflects the latest updated state of the hierarchy ?


'''




class Group:
    def __init__(self, name) -> None:
        self.name = name
        self.parent = []
        self.children = []
        self.employees = []


class Directory:
    def __init__(self) -> None:
        self.group_map = {}
        self.employee_to_group = {}
        pass

    

    def get_or_create_group(self, group_name):
        if group_name not in self.group_map:
            group = Group(group_name)
            self.group_map[group_name] = group
        group = self.group_map[group_name]
        return group
    def add_group(self, child_group, parent_group):
        child = self.get_or_create_group(child_group)
        parent = self.get_or_create_group(parent_group)
        child.parent.append(parent)
        parent.children.append(child)
    
    def add_employee(self, emp_name, group_name):
        group = self.get_or_create_group(group_name)
        self.employee_to_group[emp_name] = group
        group.employees.append(emp_name)
    

    def dfs(self, group, visited):
        if group.name in visited:
            return
        visited.add(group.name)
        for parent in group.parent:
            self.dfs(parent, visited)
        
        return visited
    
    
    def find_common_group(self, employees = []):
        """
        Find the closest common parent group for a list of employees.
        
        Args:
            employees (list): List of employee names
            
        Returns:
            str: Name of the closest common parent group, or None if not found
        """
        if not employees:
            return None
            
        # Get all ancestor groups (including the employee's own group) for each employee
        common_set = []
        for emp in employees:
            if emp not in self.employee_to_group:
                return None  # Employee not found
                
            visited = set()
            group = self.employee_to_group[emp]
            ancestor = self.dfs(group, visited) or set()
            ancestor.add(group.name)  # Include the employee's own group
            common_set.append(ancestor)

        # Find the intersection of all ancestor sets to get common groups
        if not common_set:
            return None
            
        common_groups = set.intersection(*common_set)
        if not common_groups:
            return None
            
    
        # Find the group with the longest path from the root
        # This will be the lowest/closest common ancestor
        result = None
        max_depth = -1
        
        for group in common_groups:
            # Calculate the maximum depth considering all possible parent paths
            max_group_depth = self._calculate_max_depth(self.group_map[group])
            
            # Update result if this group is deeper
            if max_group_depth > max_depth:
                max_depth = max_group_depth
                result = group
                
        return result
    
    def _calculate_max_depth(self, group):
        """
        Calculate the maximum depth of a group considering all possible parent paths.
        A higher depth means the group is further from the root (closer to employees).
        
        Args:
            group (Group): The group to calculate depth for
            
        Returns:
            int: The maximum depth of the group
        """
        # Base case: if no parents, depth is 0
        if not group.parent:
            return 0
            
        # Calculate depth for each parent path and return the maximum
        max_parent_depth = 0
        for parent in group.parent:
            parent_depth = 1 + self._calculate_max_depth(parent)  # 1 for current level + parent's depth
            max_parent_depth = max(max_parent_depth, parent_depth)
            
        return max_parent_depth
        
            

        




# Example usage
if __name__ == "__main__":
    directory = Directory()

    # Create organization structure
    directory.add_group("SEM", "CTO")
    directory.add_group("EM", "SEM")
    directory.add_group("EM", "CTO")  # Note: This creates multiple parents for EM

    # Add employees
    directory.add_employee("subhash", "EM")
    directory.add_employee("sahu", "SEM")

    # Print the directory structure
    print("Group Map:", directory.group_map)
    print("Employee to Group Map:", directory.employee_to_group)

    # Find and print the common group
    common_group = directory.find_common_group(["subhash", "sahu"])
    print(f"\nClosest common parent group: {common_group}")


        

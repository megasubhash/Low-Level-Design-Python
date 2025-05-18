from collections import defaultdict, deque

class Group:
    def __init__(self, name):
        self.name = name
        self.employees = []
        self.children = []
        self.parents = []

class OrgHierarchyDAG:
    def __init__(self):
        self.groups = {}
        self.emp_to_group = {}

    def get_or_create_group(self, name):
        if name not in self.groups:
            self.groups[name] = Group(name)
        return self.groups[name]

    def add_group_relation(self, parent_name, child_name):
        parent = self.get_or_create_group(parent_name)
        child = self.get_or_create_group(child_name)
        parent.children.append(child)
        child.parents.append(parent)

    def add_employee(self, emp_name, group_name):
        group = self.get_or_create_group(group_name)
        group.employees.append(emp_name)
        self.emp_to_group[emp_name] = group

    def find_ancestors(self, group):
        visited = set()
        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for parent in node.parents:
                dfs(parent)
        dfs(group)
        return visited

    def find_common_group(self, employees):
        ancestor_sets = []
        for emp in employees:
            group = self.emp_to_group[emp]
            ancestors = self.find_ancestors(group)
            ancestors.add(group)  # Include the group itself
            ancestor_sets.append(ancestors)

        common = set.intersection(*ancestor_sets)

        if not common:
            return None

        # Now select the deepest group among the common ones
        def get_depth(group):
            visited = {}
            def dfs(g):
                if g in visited:
                    return visited[g]
                max_depth = 0
                for parent in g.parents:
                    max_depth = max(max_depth, dfs(parent) + 1)
                visited[g] = max_depth
                return max_depth
            return dfs(group)

        return max(common, key=get_depth)

org = OrgHierarchyDAG()

# Build group DAG
org.add_group_relation("A", "B")
org.add_group_relation("A", "C")
org.add_group_relation("B", "D")
org.add_group_relation("C", "D")  # D has two parents: B and C
org.add_group_relation("C", "E")

# Add employees
org.add_employee("alice", "D")
org.add_employee("bob", "E")

# Find closest common parent group
common_group = org.find_common_group(["alice", "bob"])
print("LCA group (DAG):", common_group.name if common_group else "None")
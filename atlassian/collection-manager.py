
'''

Imagine we have a system that stores files, and these files can be grouped into collections. We are interested in knowing where our resources are being taken up.

For this system we would like to generate a report that lists:

The total size of all files stored; and

The top N collections (by file size) where N can be a user-defined value

An example input into your report generator might look like:



file1.txt (size: 100)
file2.txt (size: 200) in collection "collection1"
file3.txt (size: 200) in collection "collection1"
file4.txt (size: 300) in collection "collection2"
file5.txt (size: 10)
You should encourage candidates to transform the above into an in-memory representation of their choice (e.g. listOf(File("file1.txt", 100, null), …)). We are not expecting candidates to parse the above input, so guide them away from that.

Some candidates equate “collection” with “folder” which is not quite the right mental model. It can sometimes be helpful to clarify by saying something along the lines of “you can think of collections as being like tags for files”.

Files may not be in a collection. How does the candidate deal with that? Do they pick up on it?

A basic solution can be arrived at by using a map to store the size of each collection and accumulate into that map through a single pass over the input files. The ordered list of collections can be obtained by sorting the map on the value.

An example (basic) solution might look like:

The scenario can be extended by allowing files to be in multiple collections at once (e.g. treat collections more like tags).

In this case we want the collection size to be the total size of all files in the collection itself. However we want the “total” size reported to include each file only once.

The input data here might look like:



file1.txt (size: 100)
file2.txt (size: 200) in collection "collection1"
file3.txt (size: 200) in collection "collection1"
file4.txt (size: 300) in collection "collection2" and "collection3"
file5.txt (size: 10)
Depending on how the original implementation was modeled, this change may be simple to make (e.g. just update multiple collection sizes as you iterate) or reasonably complex (if they have chosen to hold a “file” object as a child of a “collection” object in a graph).

Level 2: Hierarchical collections

Extend the scenario by allowing collections to contain other collections. The size of a collection is the total size of all of its child collections, plus the total size of any files in the collection itself.

The input data for this extension might look like:



files:
file1.txt (size: 100)
file2.txt (size: 200) in collection "collection1"
file3.txt (size: 200) in collection "collection1"
file4.txt (size: 300) in collection "collection2" and "collection3"
file5.txt (size: 10)
collections:
"collection1" has no parent
"collection2" has parent "collection1"
"collection3" has no parent
A solution to this extension is to model collections as a tree or a graph and to calculate the collection size recursively (using a depth-first or breadth-first traversal).

'''



import collections
from heapq import heappop, heappush, nlargest


class CollectionManager:
    def __init__(self, top_k, files, tags) -> None:
        self.top_k = top_k
        self.collection_to_file = collections.defaultdict(list)
        self.total_size = self._map_files(files)
        self.collection_map = collections.defaultdict(list)
        self.collection_size = collections.defaultdict(int)
        self.all_collections = set()
        self._map_collection(tags)
        self.get_collection_size()
        pass

    def _map_files(self, files):
        total_size = 0
        for file in files:
            total_size += file["size"]
            for collection in file["collection"]:
                self.collection_to_file[collection].append((file["size"], file["name"]))
        return total_size
    
    def _map_collection(self, tags):

        for tag in tags:
            self.all_collections.add(tag["name"])
            if tag["parent"]:
                self.collection_map[tag["parent"]].append(tag["name"])

    def calculate_size(self):
        return self.total_size
        pass
    
    def get_collection_size(self):
        visited = set()
        for coll in self.all_collections:
            if coll not in visited:
                self.dfs(coll, visited)
        
    
    def dfs(self, collection, visited):
        if collection in visited:
            return 0
        visited.add(collection)

        size = sum([s for s, _ in  self.collection_to_file[collection]])

        for child in self.collection_map[collection]:
            size += self.dfs(child, visited)
        
        self.collection_size[collection] = size
        return size


    def get_top_files_v2(self, k):
        max_heap = []

        for coll, total_size in self.collection_size.items():
           
            heappush(max_heap, (-total_size, coll))
        
        res = []
        while k:
            size, coll = heappop(max_heap)
            res.append((coll, -size))
            k -= 1
        return res

    def get_top_files(self, k):
        max_heap = []

        for coll, files in self.collection_to_file.items():
            total_size = 0
            for size, file in files:
                total_size += size
            
            heappush(max_heap, (-total_size, coll))
        
        res = []
        while k:
            size, coll = heappop(max_heap)
            res.append((coll, -size))
            k -= 1
        return res



files = [
    {
        "name": "file1.txt",
        "size": 100,
        "collection":[None]
    },
    {
        "name": "file2.txt",
        "size": 200,
        "collection":["collection1"]
    },
    {
        "name": "file3.txt",
        "size": 200,
        "collection":["collection1"]
    },
    {
        "name": "file4.txt",
        "size": 200,
        "collection":["collection2", "collection3"]
    },
    {
        "name": "file5.txt",
        "size": 10,
        "collection":[None]
    }
]

tags = [
    {"name": "collection1", "parent": None},
    {"name": "collection2", "parent": "collection1"},
    {"name": "collection3", "parent": None}
]

manager = CollectionManager(2, files, tags)

print(manager.total_size)
print(manager.get_top_files_v2(2))
print(manager.collection_size)
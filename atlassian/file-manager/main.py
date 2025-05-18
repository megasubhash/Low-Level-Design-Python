from typing import List, Dict, Optional
import heapq
from collections import defaultdict

# Define File and Collection models
class File:
    def __init__(self, name: str, size: int, collections: Optional[List[str]] = None):
        self.name = name
        self.size = size
        self.collections = collections if collections else []

class CollectionManagerLevel1:
    """
    Level 1: Basic collections (each file belongs to 0 or 1 collection)
    """
    def __init__(self, files: List[File], top_n: int):
        self.files = files
        self.top_n = top_n

    def generate_report(self):
        total_size = 0
        collection_sizes = defaultdict(int)

        for file in self.files:
            total_size += file.size
            for col in file.collections:
                if col:  # skip None
                    collection_sizes[col] += file.size

        # Get top N collections by size using a heap
        top_collections = heapq.nlargest(self.top_n, collection_sizes.items(), key=lambda x: x[1])

        return total_size, top_collections

class CollectionManagerLevel2(CollectionManagerLevel1):
    """
    Level 2: Files can be in multiple collections, but total size is only counted once.
    """
    def generate_report(self):
        total_size = 0
        collection_sizes = defaultdict(int)
        visited_files = set()

        for file in self.files:
            if file.name not in visited_files:
                total_size += file.size
                visited_files.add(file.name)
            for col in file.collections:
                if col:
                    collection_sizes[col] += file.size

        top_collections = heapq.nlargest(self.top_n, collection_sizes.items(), key=lambda x: x[1])
        return total_size, top_collections

class CollectionManagerLevel3:
    """
    Level 3: Hierarchical collections with DFS
    """
    def __init__(self, files: List[File], top_n: int, collection_parents: Dict[str, Optional[str]]):
        self.files = files
        self.top_n = top_n
        self.collection_parents = collection_parents
        self.collection_graph = defaultdict(list)
        self.collection_files = defaultdict(list)
        self.collection_size_cache = {}

        self._build_graph()

    def _build_graph(self):
        # Build graph from child -> parent
        for collection, parent in self.collection_parents.items():
            if parent:
                self.collection_graph[parent].append(collection)

        for file in self.files:
            for col in file.collections:
                if col:
                    self.collection_files[col].append(file.size)

    def _dfs(self, collection: str) -> int:
        if collection in self.collection_size_cache:
            return self.collection_size_cache[collection]

        total_size = sum(self.collection_files[collection])
        for child in self.collection_graph[collection]:
            total_size += self._dfs(child)

        self.collection_size_cache[collection] = total_size
        return total_size

    def generate_report(self):
        total_size = sum(file.size for file in self.files)

        all_collections = set(self.collection_parents.keys())
        for collection in all_collections:
            self._dfs(collection)

        top_collections = heapq.nlargest(self.top_n, self.collection_size_cache.items(), key=lambda x: x[1])
        return total_size, top_collections


# Sample Input
files = [
    File("file1.txt", 100),
    File("file2.txt", 200, ["collection1"]),
    File("file3.txt", 200, ["collection1"]),
    File("file4.txt", 300, ["collection2", "collection3"]),
    File("file5.txt", 10)
]

collection_parents = {
    "collection1": None,
    "collection2": "collection1",
    "collection3": None
}

# Run all levels
level1 = CollectionManagerLevel1(files, 2)
level2 = CollectionManagerLevel2(files, 2)
level3 = CollectionManagerLevel3(files, 2, collection_parents)

level1_report = level1.generate_report()
level2_report = level2.generate_report()
level3_report = level3.generate_report()

print(level1_report, level2_report, level3_report)

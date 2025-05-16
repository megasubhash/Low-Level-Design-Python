
# file1.txt (size: 100)
# file2.txt (size: 200) in collection "collection1"
# file3.txt (size: 200) in collection "collection1"
# file4.txt (size: 300) in collection "collection2" and "collection3"
# file5.txt (size: 10)




import collections


class CollectionManager:
    def __init__(self, top_k, files) -> None:
        self.top_k = top_k
        self.collection_to_file = collections.defaultdict(list)
        self.total_size = self._map_files(files)
        pass

    def _map_files(self, files):
        total_size = 0
        for file in files:
            total_size += file["size"]
            for collection in file["collection"]:
                self.collection_to_file[collection].append((file["size"], file["name"]))
        return total_size

    def calculate_size(self):
        return self.total_size
        pass

    def get_top_files(self):
        return []



collection = [
    {
        "name":"",
        "parent": None
    }
]
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

manager = CollectionManager(2, files)

print(manager.total_size)
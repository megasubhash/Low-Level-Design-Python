import collections


class TrieNode:
    def __init__(self) -> None:
        self.val = None
        self.children = collections.defaultdict(TrieNode)
        self.is_word = False

class Router:
    def __init__(self) -> None:
        self.root = TrieNode()

    
    def add_route(self, path, val):
        node = self.root
        for ch in path.strip("/").split("/"):
           
            node = node.children[ch]

        node.val = val
    
    def _dfs(self, node, segments, index = 0):
        if not node:
            return
        if index >= len(segments):
            return node.val
        
        seg = segments[index]
        res = None

        if seg in node.children:
            res = self._dfs(node.children[seg], segments, index + 1)
            if res:
                return res

        if "*" in node.children:
            res = self._dfs(node.children["*"], segments, index + 1)
            if res:
                return res
            
        return None
    
    def call_route(self, path):
        return self._dfs(self.root, path.strip("/").split("/"))
        pass


router = Router()
router.add_route("/foo", "foo")
router.add_route("/bar/*/baz", "bar")

print(router.call_route("/foo"))          # "foo"
print(router.call_route("/bar/a/baz"))    # "bar"
print(router.call_route("/bar/x/y"))      # None

router = Router()
router.add_route("/foo/baz", "foo")
router.add_route("/foo/*", "bar")

print(router.call_route("/foo/baz"))      # "foo" (exact match wins)
print(router.call_route("/foo/test")) 
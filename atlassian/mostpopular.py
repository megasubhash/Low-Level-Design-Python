
import collections

class Node:
    def __init__(self, freq):
        self.freq = freq
        self.prev = None
        self.next = None
        self.keys = set()

class MostPopular:
    def __init__(self):
        self.char_map = {}  # char -> Node
        self.head = Node(float("inf"))  # Dummy head for max
        self.tail = Node(float("-inf")) # Dummy tail for min
        self.head.prev = self.tail
        self.tail.next = self.head

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_node_after(self, node, prev_node):
        node.next = prev_node.next
        node.prev = prev_node
        prev_node.next.prev = node
        prev_node.next = node

    def increase(self, char):
        if char in self.char_map:
            node = self.char_map[char]
            node.keys.remove(char)
            next_freq = node.freq + 1

            if node.next.freq != next_freq:
                new_node = Node(next_freq)
                self._add_node_after(new_node, node)
            else:
                new_node = node.next

            new_node.keys.add(char)
            self.char_map[char] = new_node

            if not node.keys:
                self._remove_node(node)
        else:
            if self.tail.next.freq != 1:
                new_node = Node(1)
                self._add_node_after(new_node, self.tail)
            else:
                new_node = self.tail.next
            new_node.keys.add(char)
            self.char_map[char] = new_node

    def decrease(self, char):
        if char not in self.char_map:
            return

        node = self.char_map[char]
        node.keys.remove(char)
        new_freq = node.freq - 1

        if new_freq == 0:
            del self.char_map[char]
        else:
            if node.prev.freq != new_freq:
                new_node = Node(new_freq)
                self._add_node_after(new_node, node.prev)
            else:
                new_node = node.prev
            new_node.keys.add(char)
            self.char_map[char] = new_node

        if not node.keys:
            self._remove_node(node)

    def get_max(self):
        return next(iter(self.head.prev.keys)) if self.head.prev != self.tail else ""

    def get_min(self):
        return next(iter(self.tail.next.keys)) if self.tail.next != self.head else ""


most_popular = MostPopular()
most_popular.increase("S")
most_popular.increase("S")
most_popular.increase("D")
most_popular.increase("D")
most_popular.decrease("D")
most_popular.decrease("D")
print(most_popular.get_max())
print(most_popular.get_min())
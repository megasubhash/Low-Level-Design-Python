

import collections
from heapq import heappop, heappush


class RatingManager:
    def __init__(self) -> None:
        self.rating_map = collections.defaultdict(lambda: [0, 0])
        self.min_rating = 1
        self.max_rating = 10
        pass
    
    def give_rating(self, name, rating):
        if not (self.min_rating <= rating <= self.max_rating):
            raise ValueError("Invalid Rating")
        prev_total_rating, prev_count = self.rating_map[name]

        self.rating_map[name] = [prev_total_rating + rating, prev_count + 1]

    def get_ratings(self):
        max_heap = []

        for name, (total_rating, total_count) in self.rating_map.items():
            heappush(max_heap, ( -total_rating/total_count, -total_count, name))
        
        res = []

        while max_heap:
            rating, _, name = heappop(max_heap)
            res.append((name, -rating))
        return res

# sys = RatingManager()





# sys.give_rating("Alice", 5)
# sys.give_rating("Bob", 3)
# sys.give_rating("Bob", 10)
# sys.give_rating("Alice", 4)

# print(sys.get_ratings())
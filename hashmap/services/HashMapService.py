import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.HashMap import HashMap

class HashMapService:
    @staticmethod
    def resize_if_needed(hash_map, threshold=0.75):
        load_factor = hash_map.size / hash_map.capacity
        if load_factor >= threshold:
            # Create new hashmap with double capacity
            new_capacity = hash_map.capacity * 2
            new_hash_map = HashMap(new_capacity, hash_map.hashing_strategy)
            
            # Rehash all entries
            for bucket in hash_map.buckets:
                current = bucket
                while current:
                    new_hash_map.put(current.key, current.value)
                    current = current.next
            
            # Update original hashmap
            hash_map.buckets = new_hash_map.buckets
            hash_map.capacity = new_capacity

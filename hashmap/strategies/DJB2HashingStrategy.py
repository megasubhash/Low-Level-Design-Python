import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.HashingStrategy import HashingStrategy

class DJB2HashingStrategy(HashingStrategy):
    def hash(self, key):
        # DJB2 hash algorithm
        if isinstance(key, str):
            hash_value = 5381
            for c in key:
                hash_value = ((hash_value << 5) + hash_value) + ord(c)
            return hash_value & 0xFFFFFFFF
        return hash(key)

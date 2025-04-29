import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.HashingStrategy import HashingStrategy

class SimpleHashingStrategy(HashingStrategy):
    def hash(self, key):
        if isinstance(key, int):
            return key
        if isinstance(key, str):
            # Simple sum of character codes
            return sum(ord(c) for c in key)
        # Default to Python's hash
        return hash(key)

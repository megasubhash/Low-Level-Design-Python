import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.HashMap import HashMap
from strategies.SimpleHashingStrategy import SimpleHashingStrategy
from strategies.DJB2HashingStrategy import DJB2HashingStrategy
from enums.HashMapType import HashMapType

class HashMapFactory:
    @staticmethod
    def create_hash_map(hash_map_type=HashMapType.SIMPLE, initial_capacity=10):
        if hash_map_type == HashMapType.SIMPLE:
            return HashMap(initial_capacity, SimpleHashingStrategy())
        elif hash_map_type == HashMapType.DJB2:
            return HashMap(initial_capacity, DJB2HashingStrategy())
        else:
            return HashMap(initial_capacity)

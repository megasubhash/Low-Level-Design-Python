import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.HashNode import HashNode
from strategies.HashingStrategy import HashingStrategy
from interfaces.IHashMap import IHashMap

class HashMap(IHashMap):
    def __init__(self, capacity=10, hashing_strategy=None):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity
        self.hashing_strategy = hashing_strategy
        
    def get_hash(self, key):
        if self.hashing_strategy:
            return self.hashing_strategy.hash(key) % self.capacity
        # Default hash function
        return hash(key) % self.capacity
    
    def put(self, key, value):
        index = self.get_hash(key)
        
        if self.buckets[index] is None:
            self.buckets[index] = HashNode(key, value)
            self.size += 1
            return
            
        current = self.buckets[index]
        
        # Check if key already exists
        while current:
            if current.key == key:
                current.value = value  # Update value
                return
            if current.next is None:
                break
            current = current.next
            
        # Add to the end of the linked list
        current.next = HashNode(key, value)
        self.size += 1
    
    def get(self, key):
        index = self.get_hash(key)
        
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
            
        return None
    
    def remove(self, key):
        index = self.get_hash(key)
        
        prev = None
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
            
        return False
    
    def contains_key(self, key):
        return self.get(key) is not None
    
    def is_empty(self):
        return self.size == 0
    
    def get_size(self):
        return self.size

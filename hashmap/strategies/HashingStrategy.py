from abc import ABC, abstractmethod

class HashingStrategy(ABC):
    @abstractmethod
    def hash(self, key):
        pass

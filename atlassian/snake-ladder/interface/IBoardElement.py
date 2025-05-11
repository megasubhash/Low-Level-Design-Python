

from abc import ABC, abstractmethod
class IBoardElement(ABC):

    @abstractmethod
    def move(self):
        pass

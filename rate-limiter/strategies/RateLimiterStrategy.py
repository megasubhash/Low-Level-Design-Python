

from abc import abstractmethod, ABC


class RateLimiterStrategy(ABC):
    @abstractmethod
    def is_allowed():
        pass
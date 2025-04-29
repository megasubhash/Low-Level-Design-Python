
from enum import Enum


class RateLimiterType(Enum):

    FIXED_WINDOW = "FIXED_WINDOW"
    TOKEN_BUCKET = "TOKEN_BUCKET"
    SLIDING_WINDOW = "SLIDING_WINDOW"
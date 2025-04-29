class RateLimiter:
    def __init__(self, strategy) -> None:
        self.strategy = strategy
        pass
    

    def is_allowed(self, request):
        return self.strategy.is_allowed(request)
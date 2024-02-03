import time
from threading import Lock


class RateLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.lock = Lock()

    def refill_bucket(self):
        now = time.time()
        tokens_to_add = int((now - self.last_refill_time) * self.refill_rate)
        with self.lock:
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill_time = now

    def make_request(self):
        self.refill_bucket()
        with self.lock:
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False


class RateLimitExceededException(Exception):
    """Exception raised when the rate limit is exceeded."""

    def __init__(self, message="Rate limit exceeded"):
        self.message = message
        super().__init__(self.message)

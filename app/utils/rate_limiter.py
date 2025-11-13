import time
import threading

class TokenBucket:
    def __init__(self, rate: int, capacity: int):
        self.rate = rate            # 每秒生成多少令牌
        self.capacity = capacity    # 一共最多能有多少令牌
        self.tokens = capacity
        self.timestamp = time.time()
        self.lock = threading.Lock()

    def allow(self) -> bool:
        with self.lock:
            now = time.time()

            # 根据时间增加令牌
            elapsed = now - self.timestamp
            self.timestamp = now

            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False

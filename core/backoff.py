class ExponentialBackoff:
    def __init__(self, base_delay=1.0, max_delay=30.0):
        if base_delay <= 0:
            raise ValueError("base_delay must be greater than 0")

        if max_delay < base_delay:
            raise ValueError("max_delay must be greater than or equal to base_delay")

        self.base_delay = base_delay
        self.max_delay = max_delay
        self.attempt = 0

    def next_delay(self):
        delay = min(
            self.base_delay * (2**self.attempt),
            self.max_delay,
        )

        self.attempt += 1
        return delay

    def reset(self):
        self.attempt = 0

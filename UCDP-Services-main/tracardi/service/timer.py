from collections import defaultdict
from time import time


class Timer:

    def __init__(self):
        self.time_db = defaultdict(float)

    def reset_timer(self, key):
        self.time_db[key] = time()

    def get_time(self, key) -> float:
        print(self.time_db)
        return self.time_db.get(key, 0.0)

    def is_time_over(self, key, max_time) -> bool:
        return time() - self.time_db.get(key, 0) > max_time
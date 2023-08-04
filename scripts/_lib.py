import heapq
import time

class IndexSet:
    """
    A set of indices that maintains a maximum size by removing the smallest
    index when the maximum size is reached.
    """

    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.set = set()
        self.heap = []

    def add(self, index):
        if index in self.set:
            return

        self.set.add(index)
        heapq.heappush(self.heap, index)
        if len(self.heap) > self.max_size:
            self.set.remove(heapq.heappop(self.heap))

    def __contains__(self, item):
        return item in self.set


class RateTracker:
    """
    Tracks the total count and recent rate of ticks over time, printing a
    message every interval.
    """

    def __init__(self, label="Ticks", interval=10000):
        self.label = label
        self.interval = interval
        self._reset()

    def tick(self):
        self.ticks += 1
        if self.ticks % self.interval == 0:
            rate = round(self._rate())
            print(f"{self.label}: {self.ticks} ({rate}/s)", flush=True)
            self._reset()

    def _rate(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0
        return self.ticks / elapsed_time

    def _reset(self):
        self.start_time = time.time()
        self.ticks = 0


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
        if len(self.heap) == self.max_size:
            rm_index = heapq.heappushpop(self.heap, index)
            self.set.remove(rm_index)
        else:
            heapq.heappush(self.heap, index)

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
        self.total_ticks = 0
        self._reset()

    def tick(self, n=1):
        self.ticks += n
        self.total_ticks += n
        if self.ticks >= self.interval:
            rate = "{:,}".format(round(self._rate()))
            total_ticks = "{:,}".format(self.total_ticks)
            print(f"{self.label}: {total_ticks} ({rate}/s)", flush=True)
            self._reset()

    def _rate(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0
        return self.ticks / elapsed_time

    def _reset(self):
        self.start_time = time.time()
        self.ticks = 0


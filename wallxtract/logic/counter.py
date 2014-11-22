import threading

class CounterThread(threading.Thread):
    def __init__(self, count_queue):
        threading.Thread.__init__(self)
        self.count_queue = count_queue
        self.added = 0
        self.skipped = 0

    def getAddedCount(self):
        return self.added

    def getSkippedCount(self):
        return self.skipped

    def run(self):
        while True:
            count = self.count_queue.get()
            if count == 1:
                self.added += 1
            else:
                self.skipped += 1
            self.count_queue.task_done()
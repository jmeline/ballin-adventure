__author__ = 'jmeline'
import threading

class BaseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.signal = True

    def onStart(self):
        self.signal = True

    def onStop(self):
        self.signal = False
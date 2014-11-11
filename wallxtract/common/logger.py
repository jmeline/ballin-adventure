
'''
By Jacob Meline
    Creates a factory logging method to be used within any class
'''

__author__ = 'Jacob'

import logging

class LoggerTool():
    def __init__(self):
        self.formatString = '%(asctime)s - %(levelname)s - %(name)s.%(funcName)s() (%(lineno)d): %(message)s'
        self.formatString1 = '%(asctime)s (%(levelname)s) %(module)s:%(funcName)s.%(name)s(%(lineno)d) - %(message)s'

    def setupLogger(self, loggerName, level=logging.INFO):
        l = logging.getLogger(loggerName)
        formatter = logging.Formatter(self.formatString)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(streamHandler)
        return l


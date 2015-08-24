import threading
from wallxtract.path_config import returnLogPath
from wallxtract.common.termcolor import cprint

import logging
from wallxtract.common.logger import LoggerTool
logger = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class LoggerThread(threading.Thread):
    """Log the downloaded Wallpaper"""

    def __init__(self, log_queue):
        threading.Thread.__init__(self)
        self.log_queue = log_queue
        self.logpath = returnLogPath()

    def run(self):
        while True:
            try:
                print_colored_green = lambda x: cprint(x, 'green')
                entry = self.log_queue.get()
                logger.debug("Trying to Log: %s" % entry)
                log = open(self.logpath, 'a+' )
                log.write(entry + "\n")
                log.close()
                print_colored_green("Logged: " + entry)
                self.log_queue.task_done()
            except:
                logger.error("Error in the logger")

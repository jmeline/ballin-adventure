import threading
from wallxtract.path_config import returnLogPath
from termcolor import cprint

class loggerThread(threading.Thread):
    """Log the downloaded Wallpaper"""

    def __init__(self, log_queue):
        threading.Thread.__init__(self)
        self.log_queue = log_queue
        self.logpath = returnLogPath()

    def run(self):
        while True:
            try:
                print "Trying to Log"
                print_colored_green = lambda x: cprint(x, 'green')
                entry = self.log_queue.get()
                log = open(self.logpath, 'a+' ) 
                log.write(entry + "\n")
                log.close()
                print_colored_green("Logged: " + entry)
                self.log_queue.task_done()
            except:
                print "Error in the logger"
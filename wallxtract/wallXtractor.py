import queue as Queue
import time
import logging
import requests
import sys
from termcolor import colored

from .download.download_sublink import subLinkThread
from .download.download_img import wallpaperThread

from wallxtract.parser.decrypt_sublink import decryptLinksThread

from .log.logger import loggerThread
from .counter.counter import CounterThread

from wallxtract.wallbase_config import buildUrl
from wallxtract.wallbase_config import updateUrl
from wallxtract.wallbase_config import returnThmpp


from wallxtract.common.logger import LoggerTool
logging = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class RunProgram():
    """

    """
    def __init__(self):
        self.size = 1

        self.site_queue = Queue.Queue()
        self.sublinks_queue = Queue.Queue()
        self.decryptedLinks_queue = Queue.Queue()
        self.log_queue = Queue.Queue()
        self.count_queue = Queue.Queue()
        
        self.added_imgs = 0
        self.skipped_imgs = 0

    def runThreads(self):
        for i in range(self.size):
            sl = subLinkThread(self.site_queue, self.sublinks_queue)
            dl = decryptLinksThread(self.sublinks_queue, self.decryptedLinks_queue)
            di = wallpaperThread(self.decryptedLinks_queue, self.log_queue, self.count_queue)
            logger = loggerThread(self.log_queue)

            sl.setDaemon(True)
            dl.setDaemon(True)
            di.setDaemon(True)
            logger.setDaemon(True)

            sl.start()
            dl.start()
            di.start()
            logger.start()

        countList = [CounterThread(self.count_queue) for x in range(self.size)]
        
        logging.debug("Begin counting")
        for c in countList:
            c.setDaemon(True)
            c.start()

        self.site_queue.join()
        logging.debug("Site_queue joined")
        self.sublinks_queue.join()
        logging.debug("Sublinks_queue joined")
        self.decryptedLinks_queue.join()
        logging.debug("decryptedLinks_queue joined")
        self.log_queue.join()
        logging.debug("log_queue joined")
        self.count_queue.join()
        logging.debug("count_queue joined")

        self.added_imgs, self.skipped_imgs = self.getCount(countList)

    def exists(self, path):

        r = requests.head(path)
        return r.status_code == requests.codes.ok

    def single_page(self):
        site = buildUrl()
        if not self.exists(site):
            logging.fatal("Unable to access the site, please check the url")
            sys.exit(0)


        start = time.time()
        self.site_queue.put(site)        
        self.runThreads()
        end = time.time() - start

        self.printResults(end)

    def multi_page(self): 
        pageNum = 0
        thmpp = returnThmpp()
        for i in range(1, 16):
            pageNum += int(thmpp)
            newsite = updateUrl(pageNum)
            self.site_queue.put(newsite)

        start = time.time()
        self.runThreads()
        end = time.time() - start

        self.printResults(end)

    def getCount(self, countList):
        addedCount = 0
        skippedCount = 0
        for c in countList:
            addedCount += c.getAddedCount()
            skippedCount += c.getSkippedCount()
        return addedCount, skippedCount

    def printResults(self, time):

        print_colored_magenta = lambda x: colored(x, 'magenta')
        print_colored_cyan = lambda x: colored(x, 'cyan')
        print("You have downloaded:", print_colored_magenta(self.added_imgs), "new images to your directory and skipped:", print_colored_magenta(self.skipped_imgs), "images")
        print_colored_cyan('It took:'), print_colored_magenta(time), print_colored_cyan('seconds')


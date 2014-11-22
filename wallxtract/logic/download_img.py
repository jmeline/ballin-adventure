import os
<<<<<<< HEAD:wallxtract/download/download_img.py
import re
import requests
=======
>>>>>>> Restructing code and adding json support for the configuration:wallxtract/logic/download_img.py
import logging

import requests
from termcolor import colored

from wallxtract.path_config import returnPath
from wallxtract.path_config import returnLogPath
from wallxtract.wallbase_config import returnFileLayout
<<<<<<< HEAD:wallxtract/download/download_img.py
from wallxtract.common.baseThread import BaseThread
from wallxtract.common.logger import LoggerTool
from termcolor import colored
from logic.baseThread import BaseThread
from wallxtract.common.logger import LoggerTool

log = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class wallpaperThread(BaseThread):
    """
    Download Wallpaper

    """

    def __init__(self, decryptedLinks_queue, log_queue, count_queue):
        BaseThread.__init__(self)
        self.decryptedLinks_queue = decryptedLinks_queue
        self.log_queue = log_queue
        self.count_queue = count_queue
        self.fileLayout = returnFileLayout()
        self.logpath = returnLogPath()
        self.absolutePath = returnPath() 
        
        self.path = self.absolutePath      \
                + self.fileLayout[0] + "/" \
                + self.fileLayout[1] + "/" \
                + self.fileLayout[2] + "/" 

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def isDuplicate(self, filename):
        records = open(self.logpath, 'a+')
        for f in records:
            try:
                f = f.rstrip()
                if filename == f:
                    return True
            except ValueError as e:
                log.error(e)
                return False
        return False

    def run(self):
        while self.signal:
            try:
                link = self.decryptedLinks_queue.get()
                log.debug("Trying to download image %s" % link)

                response = requests.get("http://" + link)
                
                # get file name
                filename = link.split('/')[-1]

                # check duplicates
                if not self.isDuplicate(filename):
                    self.printMsg(link, filename)
                    self.save_content(response, filename)
                    self.log_queue.put(filename)
                    self.count_queue.put(1)
                else:
                    self.count_queue.put(0)

                self.decryptedLinks_queue.task_done()
                
            except Exception as e:
                log.debug("There was an error in the image %s" % e)

    def save_content(self, resp, filename):
            save = open(self.path + filename , 'wb')
            save.write(resp.content)
            save.close()

    def printMsg(self, link, filename):
            print_colored_cyan = lambda x: colored(x, 'cyan')
            print_colored_magenta = lambda x: colored(x, 'magenta')
            print_colored_cyan("Downloading: " + link), "\n\t->", print_colored_magenta(self.path + filename) + "\n"
  
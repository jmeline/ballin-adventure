import os
import re
import requests
import logging

import requests
from wallxtract.common.termcolor import colored, cprint
from wallxtract.path_config import returnPath
from wallxtract.path_config import returnLogPath
from wallxtract.wallbase_config import returnFileLayout
from wallxtract.common.logger import LoggerTool
from .baseThread import BaseThread
from wallxtract.common.logger import LoggerTool

log = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class WallpaperThread(BaseThread):
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
            # try:
            properties = self.decryptedLinks_queue.get()
            link = properties['html']
            log.debug("Trying to download image %s" % link)

            response = requests.get(link)

            # get file name
            filename = link.split('/')[-1]

            # obtain id
            # match = re.search('-(\d*).png', filename)
            # image_id = match.group(1)

            self.printMsg(properties, filename)
            self.save_content(response, filename)
            self.log_queue.put(filename)
            self.count_queue.put(1)

            # check duplicates
            # if not self.isDuplicate(filename):
            #     self.printMsg(link, filename)
            #     self.save_content(response, filename)
            #     self.log_queue.put(filename)
            #     self.count_queue.put(1)
            # else:
            #     self.count_queue.put(0)

            self.decryptedLinks_queue.task_done()

            # except Exception as e:
            #     log.debug("There was an error in the image %s" % e)

    def save_content(self, resp, filename):
            save = open(self.path + filename , 'wb')
            save.write(resp.content)
            save.close()

    def printMsg(self, properties, filename):
            log.debug("Trying to call printMsg...[%s], [%s]" %(properties['html'], filename))
            print_colored_cyan = lambda x: cprint(x, 'cyan')
            print_colored_magenta = lambda x: cprint(x, 'magenta')

            print_colored_cyan("Downloading: " + properties['html'])
            print_colored_magenta("\n\t->" + self.path + filename)
            print_colored_magenta("\t->" + "Resolution:" + properties['Resolution'])
            print_colored_magenta("\t->" + "Size:" + properties['Size'])
            print_colored_magenta("\t->" + "Views:" + properties['Views'])
            print_colored_magenta("\t->" + "Tags:" + str(properties['Tags']))
            print_colored_magenta("\t->" + "Added:" + str(properties['Added']))

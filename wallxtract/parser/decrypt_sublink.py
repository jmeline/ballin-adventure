import re
import threading
import requests
import logging
from termcolor import cprint

from wallxtract.common.logger import LoggerTool
log = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class decryptLinksThread(threading.Thread):
    """decrypt links"""

    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        #self.pattern = r'<img src="(.*)" class="wall stage1 wide">'
        self.pattern = r'\s*<img id="wallpaper"\s*src="//(.*)"'

    def run(self):
        while True:
            try:
                link = self.in_queue.get()
                log.debug("Getting Sublink... %s" % link)
                r = requests.get(link)
                match = re.search(self.pattern, r.text)
                if match:
                    self.out_queue.put(match.group(1))
                    print_colored_yellow = lambda x: cprint(x, 'yellow')
                    print_colored_yellow("Extracted Link: " + match.group(1))
                self.in_queue.task_done()
            except:
                log.error("There was an error in getting the sublink")
                break
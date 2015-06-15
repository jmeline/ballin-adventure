import re
import sys
import requests
import logging

import requests
from termcolor import cprint
from wallxtract.common.baseThread import BaseThread

from wallxtract.common.logger import LoggerTool
from .baseThread import BaseThread

log = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

# TODO change to xpath searching instead of Regex
class SubLinkThread(BaseThread):
    """Grab Sublinks"""

    def __init__(self, site_queue, sublink_queue):
        BaseThread.__init__(self)
        self.site_queue = site_queue
        self.sublink_queue = sublink_queue
        self.wallsite = 'http://alpha.wallhaven.cc/wallpaper/'
        self.pattern = r'<a class="preview" href="http://alpha.wallhaven.cc/wallpaper/(\d*)"'
        self.sub_pattern = r'<img src="(.*)" class="wall stage1 wide">'

    def run(self):
        while self.signal:
            try:
                site = self.site_queue.get()
                log.debug("Getting Site... %s" % site)
                r = requests.get(site)
                match = re.findall ( self.pattern, r.text)
                if match:
                    for m in match:
                        link = self.wallsite + m
                        self.sublink_queue.put( link )
                self.site_queue.task_done()
            except:
                print_colored_red = lambda x: cprint (x, 'red')
                print_colored_red('Unable to connect to '+ site)
                self.site_queue.task_done()

import re
import sys
import threading
import requests
from termcolor import cprint

class subLinkThread(threading.Thread):
    """Grab Sublinks"""

    def __init__(self, site_queue, sublink_queue):
        threading.Thread.__init__(self)
        self.site_queue = site_queue
        self.sublink_queue = sublink_queue
        self.wallsite = 'http://wallbase.cc/wallpaper/'
        self.pattern = r'http://wallbase.cc/wallpaper/(\d*)'
        self.sub_pattern = r'<img src="(.*)" class="wall stage1 wide">'

    def run(self):
        while True:     
            try:
                print "Getting Site..."
                site = self.site_queue.get()
                r = requests.get(site)
                match = re.findall ( self.pattern, r.text)
                if match:
                    for m in match:
                        link = self.wallsite + m
                        self.sublink_queue.put( link )
                        #r = requests.get(link)
                        #sub_match = re.search(self.sub_pattern, r.text)
                        #if sub_match:
                        #    print_colored_yellow = lambda x: cprint(x, 'yellow')
                        #    print_colored_yellow("Extracted Link: " + sub_match.group(1))
                        #    self.sublink_queue.put( sub_match.group(1) )

                self.site_queue.task_done()
            except:
                print_colored_red = lambda x: cprint (x, 'red')
                print_colored_red('Unable to connect to '+ site)
       
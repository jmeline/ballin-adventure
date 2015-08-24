import re
import logging
import requests
from wallxtract.common.termcolor import cprint
from wallxtract.common.baseThread import BaseThread
from lxml import html
from .baseThread import BaseThread
from wallxtract.common.logger import LoggerTool

log = LoggerTool().setupLogger(__name__, level=logging.DEBUG)

class DecryptLinksThread(BaseThread):
    """decrypt links into a dictionary of properties"""

    def __init__(self, in_queue, out_queue):
        BaseThread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.pattern = r'\s*<img id="wallpaper"\s*src="//(.*)"'

    def run(self):
        while self.signal:
            link = self.in_queue.get()
            log.debug("Getting Sublink... %s" % link)
            r = requests.get(link)
            properties = self.extractProperties(r)
            self.out_queue.put(properties)
            try:
                print_colored_yellow = lambda x: cprint(x, 'yellow')
                print_colored_yellow("Extracted Link: " + properties['html'])
                #match = re.search(self.pattern, r.text)
                #if match:
                #    self.out_queue.put(match.group(1))
                #    print_colored_yellow = lambda x: cprint(x, 'yellow')
                #    print_colored_yellow("Extracted Link: " + match.group(1))
                self.in_queue.task_done()
            except Exception as e:
                log.error("There was an error in getting the sublink: %s"%e)
                break

    def extractProperties(self, link):
        """XPath html extract method"""
        tree = html.fromstring(link.text)
        xpath = '//*[@id="showcase-sidebar"]/div/div[1]/div[2]/dl'
        resolution = tree.xpath(xpath+'/dd[1]/text()')
        size = tree.xpath(xpath+'/dd[2]/text()')
        category = tree.xpath(xpath+'/dd[3]/text()')
        views = tree.xpath(xpath+'/dd[4]/text()')
        favorites = tree.xpath(xpath+'/dd[5]/a/text()')
        uploaded_by = tree.xpath(xpath+'/dd[6]/a/text()')
        uploaded_by_link = tree.xpath(xpath+'/dd[6]/a/@href')
        added = tree.xpath(xpath+'/dd[7]/time/text()')
        added_datetime = tree.xpath(xpath+'/dd[7]/time/@title')
        source = tree.xpath(xpath+'/dd[8]/text()')
        HTML = tree.xpath('//*[@id="wallpaper"]/@src')
        purity = tree.xpath('//*[@id="wallpaper-purity-form"]/fieldset/label/text()')
        tags = tree.xpath('//*[@id="tags"]/*')
        tags = dict((x.attrib['data-tag-id'], x.getchildren()[0].text) for x in tags)
        source = None
#        try:
#            source = source[0].rstrip()
#        except:
#            source = source.rstrip()
        try:
            tmp = favorites[0]
        except Exception as e:
            favorites = None

        try:
            tmp = purity[0]
        except Exception as e:
            purity = None

        return {
            "Purity": purity,
            "html": "http:" + HTML[0],
            "Resolution": resolution[0],
            "Tags": tags,
            "Size": size[0],
            "Category": category[0],
            "Views": views[0],
            "Favorites": favorites,
            # "Uploaded_by": (uploaded_by[0], uploaded_by_link[0]),
            "Added": (added[0], added_datetime),
            #"Source": source
        }


#!/usr/bin/python

import sys
import os
import re
import time
import Queue
import base64
import threading

import requests

from termcolor import colored, cprint


path = './wallpapers/'
logpath = path + 'downloadedLog.txt'
#logpath = './toplist/downloaded.txt'

class subLinkThread(threading.Thread):
    """Grab Sublinks"""

    def __init__(self, site_queue, sublink_queue):
        threading.Thread.__init__(self)
        self.site_queue = site_queue
        self.sublink_queue = sublink_queue
        self.wallsite = 'http://wallbase.cc/wallpaper/'
        self.pattern = r'http://wallbase.cc/wallpaper/(\d*)'

    def run(self):
        while True:
            try:
                site = self.site_queue.get()
                r = requests.get(site)
                match = re.findall(self.pattern, r.text)
                if match:
                    for m in match:
                        self.sublink_queue.put(self.wallsite + m)
                self.site_queue.task_done()
            except:
                print_colored_red = lambda x: cprint(x, 'red')
                print_colored_red('Unable to connect to ' + site)


class decryptLinksThread(threading.Thread):
    """decrypt links"""

    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            link = self.in_queue.get()
            r = requests.get(link)
            match = re.search(r"'\+B\('(.*)'\)\+'", r.text)
            if match:
                decryptedLink = base64.b64decode(match.group(1))
                self.out_queue.put(decryptedLink)
                print_colored_yellow = lambda x: cprint(x, 'yellow')
                print_colored_yellow("Extracted Link: " + decryptedLink)
            self.in_queue.task_done()


class wallpaperThread(threading.Thread):
    """Download Wallpaper"""

    def __init__(self, decryptedLinks_queue, log_queue, count_queue, fileLayout):
        threading.Thread.__init__(self)
        self.decryptedLinks_queue = decryptedLinks_queue
        self.log_queue = log_queue
        self.count_queue = count_queue
        self.fileLayout = fileLayout
        self.path = path + self.fileLayout[0] + "/" + self.fileLayout[1] + "/" + self.fileLayout[2] + "/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def getFilename(self, link):
        pattern = r'\/wallpaper-?((.*)\w?\.([jJ]pg|[pP]ng|[gG]if)$)'
        match = re.search(pattern, link)
        if match:
            return match.group(1)
        else:
            return None

    def isDuplicate(self, filename):
        records = open(logpath, 'a+')
        for f in records:
            try:
                f = f.rstrip()
                if filename == f:
                    return True
            except ValueError:
                return False
        return False

    def run(self):
        while True:

            link = self.decryptedLinks_queue.get()
            response = requests.get(link)

            # get file name
            filename = link.split("/")[4]

            # check duplicates
            if not self.isDuplicate(filename):

                self.printMsg(link, filename)
                self.save_content(response, filename)
                self.log_queue.put(filename)
                self.count_queue.put(1)

            else:
                self.count_queue.put(0)

            self.decryptedLinks_queue.task_done()

    def save_content(self, resp, filename):
        save = open(self.path + filename, 'wb')
        save.write(resp.content)
        save.close()

    def printMsg(self, link, filename):
        print_colored_cyan = lambda x: colored(x, 'cyan')
        print_colored_magenta = lambda x: colored(x, 'magenta')
        print print_colored_cyan("Downloading: " + link), "\n\t->", print_colored_magenta(self.path + filename) + "\n"


class loggerThread(threading.Thread):
    """Log the downloaded Wallpaper"""

    def __init__(self, log_queue):
        threading.Thread.__init__(self)
        self.log_queue = log_queue

    def run(self):
        while True:
            print_colored_green = lambda x: cprint(x, 'green')
            entry = self.log_queue.get()
            log = open(logpath, 'a+')
            log.write(entry + "\n")
            log.close()
            print_colored_green("Logged: " + entry)
            self.log_queue.task_done()


class CounterThread(threading.Thread):
    def __init__(self, count_queue):
        threading.Thread.__init__(self)
        self.count_queue = count_queue
        self.added = 0
        self.skipped = 0

    def getAddedCount(self):
        return self.added

    def getSkippedCount(self):
        return self.skipped

    def run(self):
        while True:
            count = self.count_queue.get()
            if count == 1:
                self.added += 1
            else:
                self.skipped += 1
            self.count_queue.task_done()


class RunProgram():
    def __init__(self):
        self.size = 25

        self.site_queue = Queue.Queue()
        self.sublinks_queue = Queue.Queue()
        self.decryptedLinks_queue = Queue.Queue()
        self.log_queue = Queue.Queue()
        self.count_queue = Queue.Queue()

        #site = 'http://wallbase.cc/toplist/0/123/eqeq/0x0/0/100/60/1d'

        self.added_imgs = 0
        self.skipped_imgs = 0

        self.pageNum = 0
        self.category = 'toplist'
        self.amount_per_page = str(self.pageNum)
        self.quality_preference = '213'
        self.resolution = '0x0'
        self.aspectRatio = '0'
        self.purity = '100'
        self.thmpp = '60'
        self.best_wallpapers = '0'
        self.fileLayout = [self.category, self.best_wallpapers, self.purity]
        self.site = 'http://wallbase.cc' + \
                    '/' + self.category + \
                    '/' + self.amount_per_page + \
                    '/' + self.quality_preference + \
                    '/' + 'eqeq' + \
                    '/' + self.resolution + \
                    '/' + self.aspectRatio + \
                    '/' + self.purity + \
                    '/' + self.thmpp + \
                    '/' + self.best_wallpapers

    def updateUrl(self, pageNum=0):
        self.amount_per_page = str(self.pageNum)
        self.site = 'http://wallbase.cc' + \
                    '/' + self.category + \
                    '/' + self.amount_per_page + \
                    '/' + self.quality_preference + \
                    '/' + 'eqeq' + \
                    '/' + self.resolution + \
                    '/' + self.aspectRatio + \
                    '/' + self.purity + \
                    '/' + self.thmpp + \
                    '/' + self.best_wallpapers

    def runThreads(self):
        for i in range(self.size):
            sl = subLinkThread(self.site_queue, self.sublinks_queue)
            dl = decryptLinksThread(self.sublinks_queue, self.decryptedLinks_queue)
            di = wallpaperThread(self.decryptedLinks_queue, self.log_queue, self.count_queue, self.fileLayout)
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

        for c in countList:
            c.setDaemon(True)
            c.start()

        self.site_queue.join()
        self.sublinks_queue.join()
        self.decryptedLinks_queue.join()
        self.log_queue.join()
        self.count_queue.join()

        self.added_imgs, self.skipped_imgs = self.getCount(countList)

    def single_page(self):
        start = time.time()
        self.site_queue.put(self.site)
        self.runThreads()
        end = time.time() - start

        self.printResults(end)

    def multi_page(self):
        for i in range(1, 20):
            self.pageNum += int(self.thmpp)
            self.updateUrl(self.pageNum)
            self.site_queue.put(self.site)

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
        print "You have downloaded:", print_colored_magenta(
            self.added_imgs), "new images to your directory and skipped:", print_colored_magenta(
            self.skipped_imgs), "images"
        print print_colored_cyan('It took:'), print_colored_magenta(time), print_colored_cyan('seconds')


def main():
    try:
        wallbaseExtractor = RunProgram()
        wallbaseExtractor.single_page()
        #wallbaseExtractor.multi_page()

    except KeyboardInterrupt:
        print "Exiting program!"
        sys.exit()


if __name__ == '__main__':
    main()

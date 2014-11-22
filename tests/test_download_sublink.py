__author__ = 'jmeline'

import threading

from logic.download_sublink import SubLinkThread
from wallxtract.wallbase_config import buildUrl

try:
    import Queue
except:
    import queue as Queue


class TestDownloadSublink:
    def setup(self):
        self.site_queue = Queue.Queue()
        self.sublinks_queue = Queue.Queue()
        site = buildUrl()
        assert site
        self.site_queue.put(site)

    def teardown(self):
        pass

    def test_sublinkThread(self):
        assert self.site_queue
        sl = SubLinkThread(self.site_queue, self.sublinks_queue)
        sl.setDaemon(True)
        sl.start()
        #assert self.site_queue.qsize() == 0
        assert sl.is_alive()
        # Stop thread
        sl.onStop()
        # Wait until the thread stops
        sl.join()
        if sl.is_alive():
            sl.join(1)
        assert threading.active_count() == 1

        #print (self.sublinks_queue.qsize())
        #print ("Thread count: %s " % threading.active_count())





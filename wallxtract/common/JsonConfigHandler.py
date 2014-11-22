__author__ = 'jmeline'

import json
import os
from collections import namedtuple


class JsonConfigHandler():
    def __init__(self):
        self.data = None
        self.extractedObject = None
        self._extractJson()

    def _extractJson(self):
        f = None
        try:
            print(os.path.join(os.getcwd(), "config.json"))
            f = open(os.path.join(os.getcwd(), "config.json"))
        except:
            print ("Error, no Configuration was found")

        self.data = json.load(f)
        self.extractedObject = namedtuple('Config', self.data)(**self.data)

    def wallhaven_URL(self):
        """ Create URL
        :return:
        """

        url = "http://alpha.wallhaven.cc/wallpaper/search?categories=111&purity=100&sorting=random&order=desc&page=1",

        return url

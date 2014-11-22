#!/usr/bin/env python

## main

import sys
import os

#path = os.path.expanduser('~/mystuff/Python/PythonPractice/WallXtract/')
#path = os.path.join('.', 'WallXtract')
#sys.path.append(path)
from common import JsonConfigHandler as jch

import wallxtract.wallXtractor as wallxtract
import logging
from wallxtract.common.logger import LoggerTool
log= LoggerTool().setupLogger(__name__, level=logging.DEBUG)

def main():
    try:
        config = jch.JsonConfigHandler()
        wallbaseExtractor = wallxtract.Initiate(config)
        #wallbaseExtractor.single_page()
        #wallbaseExtractor.multi_page()
        wallbaseExtractor.single_img()

    except KeyboardInterrupt:
       logging.debug("Exiting program!")
       sys.exit()

if __name__ == '__main__':
    main()


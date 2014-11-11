#!/usr/bin/env python

## main

import sys
import os

#path = os.path.expanduser('~/mystuff/Python/PythonPractice/WallXtract/')
#path = os.path.join('.', 'WallXtract')
#sys.path.append(path)

import wallxtract
import logging
from wallxtract.common.logger import LoggerTool
log= LoggerTool().setupLogger(__name__, level=logging.DEBUG)

def main():
    try:
        wallbaseExtractor = wallxtract.RunProgram()
        wallbaseExtractor.single_page()
        #wallbaseExtractor.multi_page()

    except KeyboardInterrupt:
       logging.debug("Exiting program!")
       sys.exit()
if __name__ == '__main__':
    main()


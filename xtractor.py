#!/usr/bin/env python

## main

import sys
import os

#path = os.path.expanduser('~/mystuff/Python/PythonPractice/WallXtract/')
#path = os.path.join('.', 'WallXtract')
#sys.path.append(path)

import wallxtract

def main():
    try:
        wallbaseExtractor = wallxtract.RunProgram()
        wallbaseExtractor.single_page()
        #wallbaseExtractor.multi_page()

    except KeyboardInterrupt:
       print "Exiting program!"
       sys.exit()
if __name__ == '__main__':
    main()


ballin-adventure
================
![alt tag](http://alpha.wallhaven.cc/images/layout/logo.png)

* Wallpaper downloader for wallhaven.cc (RIP wallbase.cc)
* Uses multiple threads to do maximum work
* Doesn't support downloading NSFW images
* Python 3 support if running from source. Python 2 is required for pyinstaller (which is what I use to package xtractor into an executable)

Installation
============
Required packages
   * lxml
   * requests

Installation using Conda
========================
On \*unix/OSX
$ conda create -n xtractor python=2.7 requests lxml pip
$ source activate xtractor
$ python xtractor.py

On Windows
$ conda create -n xtractor python=2.7 requests lxml pip
$ activate xtractor
$ python xtractor.py



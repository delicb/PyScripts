#!/usr/bin/env python2
'''
Deletes all empty directories from provided directory.
'''
__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Jan 7, 2013"

import os
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('folders', nargs='*', default='.',
                    help='Folders to clean. Defauls to "."')
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    dest='verbose', help='Chitchat while working!')
parser.add_argument('-t', '--test', action='store_true',
                    dest='test', default=False,
                    help='Do not delete, only print what would be deleted')

options = parser.parse_args()
print options
print options.folders
for folder in options.folders:
    print '%s - %s' % (folder, os.path.abspath(folder))
    for root, dirs, files in os.walk(os.path.abspath(folder)):
        print root
        if not (len(dirs) + len(files)):
            print 'Delete %s' % root

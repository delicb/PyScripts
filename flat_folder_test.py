#! /usr/bin/env python

'''Creates test case for flat_folder.py script.

In fact, this script just creates few folder, another few folder 
inside of them and coupe of empty files inside of each folder.
'''

import os
import sys
import random

ROOT = sys.argv[1]
if os.path.exists(ROOT):
	print('File or folder "%s" allready exists. Please choose anotherone' % ROOT)
	sys.exit(1)
	
os.mkdir(ROOT)
	
#! /usr/bin/env python

__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Sep 13, 2010"

'''Creates test case for flat_folder.py script.

In fact, this script just creates few folder, another few folder 
inside of them and couple of empty files inside of each folder.
'''
import os
import sys
import random
import shutil
import time

ROOT = sys.argv[1]
DELETE_IF_EXISTS = False
if len(sys.argv) > 2:
	if sys.argv[2] == '-d':
		DELETE_IF_EXISTS = True

if os.path.exists(ROOT):
	if DELETE_IF_EXISTS:
		shutil.rmtree(ROOT)
		# give time to rmtree to delete
		time.sleep(1)
	else:
		print('File or folder "%s" allready exists. Please choose anotherone' % ROOT)
		sys.exit(1)
	
os.mkdir(ROOT)
no_of_folders = random.randint(3, 10)
for i in xrange(no_of_folders):
	no_of_files = random.randint(3, 10)
	dir = os.path.join(ROOT, '_%d' % i)
	os.mkdir(dir)
	for j in xrange(no_of_files):
		file = os.path.join(dir, '__%d.txt' % j)
		with open(file, 'w') as f:
			f.write('%d_%d' % (i, j))
		
	
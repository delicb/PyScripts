#!/usr/bin/env python

__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Sep 19, 2010"

import sys
import os
from pprint import pprint
from optparse import OptionParser

# TODO: Dodati opciju za exclude imena fajlova, exstenzija, foldera itd

USAGE = "%prog <FOLDER>"
ROOT = ""
options = None


def get_opt_parser():
	parser = OptionParser(usage=USAGE, version="%prog 0.1")
	parser.add_option("-d", "--delete", dest="delete", action="store_true", 
						default=False, help="Delete folders after flatting")
	parser.add_option("-v", "--verbose", dest="verbose", action="store_true", 
						default=False, help="Don't print status messages to stdout")
	return parser

def log(msg):
	if options.verbose:
		print(msg)
		
def get_abs_folder(folder):
	if not os.path.isabs(folder):
		folder = os.path.abspath(os.path.join(os.getcwd(), folder))
	if not os.path.isdir(folder):
		print 'Folder "%s" does not exist' % folder
		sys.exit(1)
	return folder
	

def walk(visited_folders, dirname, fnames):
	visited_folders.append(dirname)
	move_files(dirname, fnames)
	
def move_files(dirname, fnames):
	for file in fnames:
		f = os.path.join(dirname, file)
		if os.path.isfile(f):
			log("Moving file %s to %s" % (f, ROOT))
			# TODO: Zapravo move-uj fajlove
		
def delete_folders(folders):
	for folder in folders:
		log("Deleting folder %s" % folder)
		# TODO: Zapravo obrisi foldere


def main():
	global ROOT
	global options
	parser = get_opt_parser()
	(options, args) = parser.parse_args()
	if len(args) > 1:
		print("ERROR: Only one argument is allowed and that should be folder name")
		parser.print_help()
		sys.exit(2)
	ROOT = get_abs_folder(args[0])
	VISITED_FOLDERS = []
	os.path.walk(ROOT, walk, VISITED_FOLDERS)
	if options.delete:
		VISITED_FOLDERS.reverse()
		# ROOT bi trebao da bude samo na poslednjem mestu, ali posto su svi
		# podaci u njemu sad za svaki slucaj uklanjamo svaku pojavu
		while ROOT in VISITED_FOLDERS:
			try:
				VISITED_FOLDERS.remove(ROOT) 
			except ValueError, e:
				# ne bi trebalo da se desi, ali nikad se ne zna
				pass
		delete_folders(VISITED_FOLDERS)
	
if __name__ == '__main__':
	main()
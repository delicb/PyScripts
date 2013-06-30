#!/usr/bin/env python

__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Sep 13, 2010"

import sys
import os
import shutil
from optparse import OptionParser

from utils import get_abs_folder

# TODO: Dodati opciju za exclude imena fajlova, exstenzija, foldera itd

USAGE = "%prog <FOLDER>"
ROOT = ""
options = None
FILE_LIST = []

def get_opt_parser():
    parser = OptionParser(usage=USAGE, version="%prog 0.1")
    parser.add_option("-d", "--delete", dest="delete", action="store_true", 
                        default=False, help="Delete folders after flatting")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", 
                        default=False, help="Don't print status messages to stdout")
    return parser

# TODO: Zameniti ovo pravim logovanjem
def log(msg):
    if options.verbose:
        print(msg)

def walk(visited_folders, dirname, fnames):
    '''Callback for os.path.walk '''
    visited_folders.append(dirname)
    move_files(dirname, fnames)
    
def move_files(dirname, fnames):
    '''Actually moves the files (fnames) from dirname to ROOT folder.
    
    ROOT is defined as parameter when program starts.
    '''
    for file in fnames:
        dest_file = generate_unique_file_name(file)
        dest = os.path.join(ROOT, dest_file)
        f = os.path.join(dirname, file)
        if os.path.isfile(f):
            log("Moving file %s to %s" % (f, dest))
            shutil.move(f, dest)

def generate_unique_file_name(file):
    '''Generates unique file name based on given file name.
    
    If given file name is not in FILE_LIST (global variable) returns the same
    name. 
    If it is in the FILE_LIST it appendes nubmer at the end of the file name, 
    but before extension. 
    If there are more then 2 files with the same name number at the end of the 
    name will be incremented.
    
    So, if this function is called 3 times with parameter 'a.txt' results would 
    be (in this order): a.txt, a(1).txt, a(2).txt .
    
    '''
    if file not in FILE_LIST:
        FILE_LIST.append(file) 
        return file
    i = 0
    f = file
    while f in FILE_LIST:
        i += 1
        name, ext = os.path.splitext(file)
        f = '%s(%d)%s' % (name, i, ext)
    FILE_LIST.append(f)
    return f

def delete_folders(folders):
    '''Deletes folders passed. 
    
    Parameter folders should be iterable that contains
    witch folders should be deleted.'''
    for folder in folders:
        log("Deleting folder %s" % folder)
        # NOTE: Ovde namerno korisnim os.rmdir umesto shutil.rmtree, jer 
        # bi folderi trebalo da su prazni. Kad kasnije implementiram
        # exclude mehanizam ovo bi trebalo promeniti u shutil.rmtree
        os.rmdir(folder)


def main():
    global ROOT
    global options
    parser = get_opt_parser()
    (options, args) = parser.parse_args()
    if len(args) > 1:
        print("ERROR: Only one argument is allowed and that should be folder name")
        parser.print_help()
        sys.exit(2)
    if len(args) == 0:
        folder = "."
    else:
        folder = args[0]
    try:
        ROOT = get_abs_folder(folder)
    except ValueError, e:
        print str(e)
        sys.exit(1)
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
                print("Error occured (%s)" % str(e))
                sys.exit(2)
        delete_folders(VISITED_FOLDERS)
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python

__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Sep 18, 2010"

import sys
import os
import glob
import re

# Ovo bi mozda moglo da se uradi u jednom regexp-u, ali ovako ce biti mnogo
# lakse za kasnija prosirenja, a bice ih, posto ne verujem da sam ovde
# pokrio ni pola varijacija imena
REG_EXPS = [
    re.compile(r'.* ?S(?P<season>\d+)E(?P<episode>\d+).*', re.I),
    re.compile(r'.*\[?((?P<season>\d+)x(?P<episode>\d+))\]?.*', re.I),
    re.compile(r'.*(?P<season>\d)(?P<episode>\d{2}).*', re.I),
    re.compile(r'.*Series ?(?P<season>\d) ?Ep(?P<episode>\d+).*', re.I),
]

def get_abs_folder(folder='.'):
    '''Returns absolute path of provided folder.
    
    Provided path can be relative or absolute. If nothing is provided, 
    absolute path to current folder will be returned.
    
    If provided folder does not exist, ValueError will be rased.    
    '''
    if not os.path.isabs(folder):
        folder = os.path.abspath(os.path.join(os.getcwd(), folder))
    if not os.path.isdir(folder):
        raise ValueError('Folder "%s" does not exist' % folder)
    return folder

def extract_data(names):
    res = {}
    for name in names:
        for reg_exp in REG_EXPS:
            ep = reg_exp.match(name)
            if ep is not None:
                ep = ep.groupdict()
                res[(int(ep['season']), int(ep['episode']))] = name
    return res
                
def rename(from_, to):
    from_name, from_ext = os.path.splitext(from_) #@UnusedVariable
    to_name, to_ext = os.path.splitext(to) #@UnusedVariable
    
    new_name = from_name + to_ext
    print 'Renameing %s to %s' % (to, new_name)
    os.rename(to, new_name)


if len(sys.argv) > 1:
    folder = sys.argv[1]
else:
    folder = '.'
try:
    ROOT = get_abs_folder(folder)
except ValueError, e:
    print str(e)
    sys.exit(1)
    
oldwd = os.getcwd()
os.chdir(ROOT)

TITLE_FILES = glob.glob('*.srt')
AVI_FILES = glob.glob('*.avi')

print TITLE_FILES
print AVI_FILES

TITLE_DATA = extract_data(TITLE_FILES)
AVI_DATA = extract_data(AVI_FILES)

print TITLE_DATA
print AVI_DATA

for episode, avi_name in AVI_DATA.iteritems():
    subtitle_name = TITLE_DATA[episode]
    rename(avi_name, subtitle_name)

os.chdir(oldwd)


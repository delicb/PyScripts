#!/usr/bin/env python2
'''
Searches for video and subtitle files in provided folder and tries to find
matches based on there names and renames subtitle files to match corespodenting
video file.

For example, if there are two files in folder:
    The.Big.Bang.Theory.S03.E10.The.Gorilla.Experiment.HDTV.XviD-FQM.avi
    TBBT[3x10].srt
the later will be renamed to
The.Big.Bang.Theory.S03.E10.The.Gorilla.Experiment.HDTV.XviD-FQM.srt .
'''
__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Sep 18, 2010"

import sys
import os
import glob
import re
import argparse

from utils import get_abs_folder, flatten


# Maybe this can be matched in single regular expression, but this way
# is much easier and it will be easier to add support later for more
# name formats.
REG_EXPS = [
    re.compile(r'.*? ?S(?P<season>\d+)(x| )?EP?(?P<episode>\d+).*', re.I),
    re.compile(r'.*?\[?((?P<season>\d+)x(?P<episode>\d+))\]?.*', re.I),
    re.compile(r'.*?(?P<season>\d+)(?P<episode>\d{2}).*', re.I),
    re.compile(r'.*?Series ?(?P<season>\d+) ?Ep(?P<episode>\d+).*', re.I),
]

VIDEO_GLOB = ['*.avi', '*.wmv', '*.mkv', '*.mp4', ]
SUBTITLE_GLOB = ['*.srt', '*.sub']

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('folder', nargs='?', default='.',
                    help='Path to folder in witch the file are. Defaults to "."')
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    dest='verbose', help='Chitchat while working!')
parser.add_argument('-t', '--test', action='store_true',
                    dest='test', default=False,
                    help="Only print what would happen. Don't do any real work")
parser.add_argument('-s', '--sensitive', action='store_true',
                    dest='sensitive', default=False,
                    help='Quit on any sign of trouble.')

options = parser.parse_args()


# TODO: Replace this with proper logging
def log(msg):
    if options.verbose:
        print(msg)


def get_files(pattern):
    '''Returns list of files that matches glob pattern provided.

    Pattern can be iterable with multiple patterns.'''
    if not hasattr(pattern, '__iter__'):
        pattern = [pattern]
    return list(flatten([glob.glob(x) for x in pattern]))


def extract_data(names):
    '''Returns dict with data about each episode.

    Key is tuple where first value is season number, and the second value is
    episode number. Value is name of the file.
    '''
    res = {}
    for name in names:
        for reg_exp in REG_EXPS:
            ep = reg_exp.match(name)
            if ep is not None:
                ep = ep.groupdict()
                season = int(ep['season'])
                episode = int(ep['episode'])
                key = (season, episode)
                if key in res and options.sensitive:
                    raise ValueError('''Looks like files %s and %s are the same
                    episode. Please leave only valid file or not use
                    --sensitive option (in that case one of the files will
                    remain untouched''' % (name, res[key]))
                log('Found matching file %s' % name)
                res[(season, episode)] = name
    return res


def rename(from_, to):
    '''Renames `to` file based on `from_` name.

    Creates new file name that contains everything before the final dot
    (or whatever extension separator is) from `from_` and extension (and
    extension separator) from `to`.

    If file with that new name already exists raises ValueError.
    '''
    from_name = os.path.splitext(from_)[0]
    to_ext = os.path.splitext(to)[1]
    new_name = from_name + to_ext
    new_file_path = os.path.join(os.getcwd(), new_name)
    if not to == new_name:
        if os.path.exists(new_file_path):
            raise ValueError('Tried to rename {0} to {1}, but {1} already exists'.
                             format(to, new_name))
        else:
            log('Renaming %s to %s' % (to, new_name))
            if not options.test:
                os.rename(to, new_name)


def rename_all(from_, to):
    '''Maps from and to files and calls `rename` for each of them.'''
    for key, val in from_.iteritems():
        other_val = to.get(key, None)
        if other_val is not None:
            rename(val, other_val)


def main():
    oldwd = os.getcwd()
    options = parser.parse_args()
    try:
        root = get_abs_folder(options.folder)
    except ValueError, e:
        print(e)
        sys.exit(1)
    os.chdir(root)
    log('Temporarily changing working dir to %s' % root)
    video_files = get_files(VIDEO_GLOB)
    subtitle_files = get_files(SUBTITLE_GLOB)
    try:
        video_data = extract_data(video_files)
        subtitle_data = extract_data(subtitle_files)
        rename_all(video_data, subtitle_data)
    except ValueError, e:
        print(e)
        sys.exit(2)

    log('Restoring working dir to %s' % oldwd)
    os.chdir(oldwd)

if __name__ == '__main__':
    main()

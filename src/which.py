#!/usr/bin/env python2
'''
Simulation of linux which command.

Searches path to find executable with provied name and prints its full path.
'''
__author__ = "Bojan Delic <bojan@delic.in.rs>"
__date__ = "Jan 7, 2013"

import os
import argparse

__all__ = ['get_path_to_executable']

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('cmd', help='Executable to find in path')
parser.add_argument('-e', '--extensions', nargs='*', dest='extensions', 
                    help='Extensions to consider as executables. ' + 
                    'Defaults to extensions defined in environment variable PATHEXT.')

def get_path_to_executable(name, extensions=None):
    ''' Finds path to executable in path.  
    
    Simulates which command from UnixTools for windows, but does not requrie
    extension to be supplied.
    '''
    name, ext = os.path.splitext(name)
    if ext != '':
        extensions = [ext]
    elif extensions is None:
        extensions = map(lambda x: x.lower(), os.environ.get('PATHEXT').split(';'))
    for path in os.environ.get('PATH').split(';'):
        for ext in extensions:
            executable = os.path.join(path, '{0}{1}'.format(name, ext))
            if os.path.isfile(executable):
                yield executable
            
def main():
    options = parser.parse_args()
    ext = options.extensions if options.extensions is not None else None
    for executable in get_path_to_executable(options.cmd, ext):
        print executable

if __name__ == '__main__':
    main()
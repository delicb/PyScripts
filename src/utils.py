__author__ = "Bojan Delic <bojan@delic.in.rs>"

import os


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


def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem

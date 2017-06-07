# -*- coding: utf-8 -*-
"""
====================================
__init__ :mod:`downloaders.__init__`
====================================
Downloaders for GetWebFilesInator
"""
from glob import glob
import imp
import os
from os.path import basename, splitext, join, dirname
import inspect
from operator import itemgetter
from types import ModuleType
from getwebfilesinator.downloaders import downloaders_defaults as dfd
DOWNLOADERS = []

def add_downloader(name, path):
    """
    Add downloader

    :param str name: Module name.
    :param path: Source path for the module or module instance
    :type path: string or object
    """
    if (name, path) not in DOWNLOADERS:
        DOWNLOADERS.append((name, path))

def load_downloaders(client):
    """load downloaders"""
    result = []
    # for each downloader
    for downloader in DOWNLOADERS:
        # if is already a module...
        if isinstance(downloader[1], ModuleType):
            module = downloader[1]
        else:
            # else we load it from source path.
            module = imp.load_source(*downloader)
        # create a list of classes which are subclass of Downloader.
        classes = [
            c[1](client) for c in inspect.getmembers(module, inspect.isclass)
            if issubclass(c[1], dfd.Downloader) and not c[1] is dfd.Downloader]
        # append to the result.
        result += classes
    # sort result using the guess_priority
    result.sort(key=lambda c: c.guess_priority)
    return result

def add_defaults():
    """Add defaults downloaders"""
    for proc_path in glob(join(dirname(__file__), "downloaders_*.py")):
        name = splitext(basename(proc_path))[0]
        add_downloader(name, proc_path)
    add_downloader('downloaders_defaults', dfd)

# add default downloaders.
add_defaults()

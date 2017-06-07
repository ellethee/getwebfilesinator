# -*- coding: utf-8 -*-
"""
============================================================
Downloaders_defaults :mod:`downloaders.downloaders_defaults`
============================================================
Dowloader class and default downloaders
"""
from os.path import isfile
import re
is_download = re.compile(r'^https?:\/\/.+\/.+\.\w+').search

class Downloader(object):
    """
    Class for create downloaders for GetWebFilesInator
    """

    #: The client object.
    client = None
    #: The configuration object.
    cfg = None
    #: Gives a priority for the ``guess_type`` type method
    guess_priority = 0
    #: Name of the get_type used to map the downloader.
    get_type = ''

    def __init__(self, client):
        self.client = client
        self.cfg = client.cfg

    def download(self, sfile):
        """
        Process a sfile

        :param Edo sfile: a Edo object (which is a dict with attributes)
        :rtype: any.

        This method can return:

            - ``False``: if we want to stop processing the file.
            - ``True`` or ``None``: if we want the client guess the action from the filename.
            - ``'zip'`` or ``'plain'``: to force the action to take.
            - a ``callable`` which accepts ``sfile`` and ``cfg`` as parameters if we want to pass the action to take.

        """
        pass

    def guess_type(self, sfile):
        """
        Guess the get_type

        :param Edo sfile: the sfile to test.
        :rtype: self or None

        Returns ``None`` if the test on sfile fails else returns ``self``
        """
        pass

class DownloaderLocal(Downloader):
    """Process local files"""
    guess_priority = 999
    get_type = 'local'

    def download(self, sfile):
        """Process local files"""
        return isfile(sfile.filename)

    def guess_type(self, sfile):
        if not sfile.url and sfile.filename:
            return self

class DownloaderDownload(Downloader):
    """Process downloads"""
    guess_priority = 998
    get_type = 'download'

    def download(self, sfile):
        """Process download"""
        return self.client.download(sfile)

    def guess_type(self, sfile):
        if is_download(sfile.url or ''):
            return self

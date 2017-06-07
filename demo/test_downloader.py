# -*- coding: utf-8 -*-
"""
=============================================
Test_downloader :mod:`python.test_downloader`
=============================================

"""
from logging import getLogger
from getwebfilesinator.downloaders.downloaders_defaults import Downloader
log = getLogger(__name__)

class DownloaderTest(Downloader):
    """Test downloader"""

    get_type = 'test_download'

    def download(self, sfile):
        """Process file"""
        log.info(">>>> I'm a test downloader. No actions for me :'(")
        return False

    def guess_type(self, sfile):
        """Guess retrieve type"""
        if sfile.url == 'imatest':
            return self

class DownloaderGreet(Downloader):
    """Downloader with action included"""

    get_type = 'greet'

    def greet(self, sfile, cfg):
        """ My action """
        log.info("Now we are greeting %s", sfile.greet)

    def download(self, sfile):
        """Process sfile"""
        sfile.greet = sfile.url[8:]
        return self.greet

    def guess_type(self, sfile):
        """Guess the type"""
        if sfile.url.startswith('greet://'):
            return self

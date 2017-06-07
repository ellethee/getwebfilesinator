# -*- coding: utf-8 -*-
"""
========================================================
Downloaders_github :mod:`downloaders.downloaders_github`
========================================================
GitHub downloaders
"""
import re
from logging import getLogger
from getwebfilesinator.downloaders.downloaders_defaults import Downloader
# define some costant string
GIT_RELEASE = "https://api.github.com/repos/{}/releases/latest"
GIT_DOWNLOAD = "https://github.com/{}/archive/master.zip"
GIT_RAW = "https://raw.githubusercontent.com/{}/master/{}"
# github checker
is_github = re.compile(r'(?!^https?:\/\/)^.+\/.+?$').search
log = getLogger(__name__)


class DownloaderGitHubDownload(Downloader):
    """DownloaderGitHubDownload"""
    get_type = "github_download"
    guess_priority = 997

    def download(self, sfile):
        """Processa github download"""
        sfile.url = GIT_DOWNLOAD.format(sfile.url)
        return self.client.download(sfile)

    def guess_type(self, sfile):
        """Guess type"""
        url = GIT_DOWNLOAD.format(sfile.url)
        if re.search(GIT_DOWNLOAD.format(r'\.+?/\.+?'), url):
            return self


class DownloaderGitHubRaw(Downloader):
    """DownloaderGitHubRaw"""

    get_type = "github_raw"
    guess_priority = 995

    def download(self, sfile):
        """Processa dwnload raw"""
        sfile.url = GIT_RAW.format(sfile.url, sfile.filename)
        return self.client.download(sfile)

    def guess_type(self, sfile):
        """Guess type"""
        if is_github(sfile.url or '') and sfile.filename:
            return self


class DownloaderGitHub(Downloader):
    """DownloaderGitHu"""
    get_type = "github"
    guess_priority = 996

    def download(self, sfile):
        """Process github directly with api"""
        url = None
        # try to get assets for the release.
        release = self.client.json(GIT_RELEASE.format(sfile.url))
        assets = release.get('assets')
        version = release.get('tag_name')
        # if we don't have assets for release we try to get the master.zip
        if assets:
            # if we have more than one asset we need to filter by name or filter
            if len(assets) > 1 and sfile.filter or sfile.name:
                assets = [
                    a for a in assets
                    if re.match(sfile.filter or sfile.name, a['name'])] + assets
            # in any case we get the first one.
            url = assets[0].get('browser_download_url')
        if version:
            log.info("Version: %s", version)
        if url:
            sfile.url = url
        else:
            # if we don't have a valid url try the master.zip
            log.warn("Can't find a valid asset i'll try to download master.zip")
            sfile.url = GIT_DOWNLOAD.format(sfile.url)
        return self.client.download(sfile)

    def guess_type(self, sfile):
        """Guess type"""
        if is_github(sfile.url or '') and sfile.files:
            return self

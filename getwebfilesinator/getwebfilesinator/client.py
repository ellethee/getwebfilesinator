# -*- coding: utf-8 -*-
"""
======================================
Client :mod:`getwebfilesinator.client`
======================================
The GetWebFilesInator Client
"""
from os.path import dirname, abspath
import sys
import shutil
import tempfile
import requests
from getwebfilesinator import utils
from getwebfilesinator import classes
from getwebfilesinator import downloaders
log = utils.getLogger(__name__)


class GwfiClient(object):
    """GetWebFilesInator Client"""

    def __init__(self, cfg):
        # Instantiate a request session
        self.session = requests.Session()
        # so we can use a github authendicated sessions if username and
        # password is provided. (less problems when testing)
        if cfg.github_username and cfg.github_password:
            self.session.auth = (cfg.github_username, cfg.github_password)
        # loads extra templates blocks from configuration if any.
        utils.BLOCKS.update({k.lower(): v for k, v in cfg.get('blocks', {})})
        # Instantiate the Singleton ListKeeper class.
        classes.ListKeeper(cfg)
        # save the configuration
        self.cfg = cfg
        self.cfg.paths.gwfi = utils.GWFI_PATH
        # ok, reupdate paths.
        utils.update_paths(self.cfg.paths, self.cfg)
        # twice.. i should fix this.
        utils.update_paths(self.cfg.paths, self.cfg)
        # let's add exta downloaders defined in configuration, if any.
        for name, path in cfg.downloaders or {}:
            downloaders.add_downloader(name, path)
        # loads all the downloaders (defaults and extras)
        self.downloaders = downloaders.load_downloaders(self)
        # mapping the get_type for downloaders.
        self.get_types = {d.get_type: d for d in self.downloaders}

    def guess_downloader(self, sfile):
        """Try to guess the get_type"""
        # if our sfile has a get_type define we will use that
        if sfile.get_type in self.get_types:
            return self.get_types[sfile.get_type]
        # if not, we will cycle through all downloaders to guess the right type.
        for downloader in self.downloaders:
            if downloader.guess_type(sfile) is not None:
                return downloader

    def get(self, url, **kwargs):
        """wrapper for requests.Session.get"""
        return self.session.get(url, **kwargs)

    def json(self, url, **kwargs):
        """wrapper for requests.Session.get and json conversion."""
        try:
            return self.session.get(url, **kwargs).json()
        except StandardError:
            return {}

    def process(self, files):
        """Process all the *files* in the configuration"""
        for sfile in files:
            # update the sfile paths
            utils.update_paths(self.cfg.paths, sfile)
            # create a tmp directory for any operation
            sfile.tmpdir = tempfile.mkdtemp(prefix="gwfi_")
            log.debug("TMP: %s", sfile.tmpdir)
            # let's guess the downloader for the sfile.
            downloader = self.guess_downloader(sfile)
            # if don't have a dowloader we will rise an AttributeError.
            if not downloader:
                msg = "Can't find a downloader for type: {}".format(
                    sfile.get_type or '')
                log.error(msg)
                raise AttributeError(msg)
            # else we'll go on with the processing
            log.info("Processing %s: %s", downloader.get_type, sfile.url or
                     sfile.filename)
            # if the download method of the downloader is True we'll go on with
            # the processing.
            result = downloader.download(sfile)
            if result is not False:
                # get the action function by result.
                if callable(result):
                    func = result
                elif result == 'zip':
                    func = utils.process_zip
                elif result == 'plain':
                    func = utils.process_plain
                else:
                    # try to process a zip file, if it is.
                    if sfile.filename.endswith('.zip'):
                        func = utils.process_zip
                    else:
                        # else it must be a sigle file.
                        func = utils.process_plain
                try:
                    func(sfile, self.cfg)
                except StandardError as error:
                    # in case of error we log it and raise it.
                    log.exception(error)
                    raise
                finally:
                    # anyway, if we didn't decide to keep it we will delete the
                    # temp folder.
                    if not self.cfg.keep:
                        shutil.rmtree(sfile.tmpdir, ignore_errors=True)
            else:
                # if we didn't decide to keep it we will delete the
                # temp folder.
                if not self.cfg.keep:
                    shutil.rmtree(sfile.tmpdir, ignore_errors=True)
        # try to write the html files using the templates.
        utils.write_html(self.cfg)


    def download(self, sfile):
        """Our download method"""
        log.debug(sfile.url)
        # check if url is cached and get the ondisk filename.
        cached, sfile.filename = utils.is_cached(sfile, self.cfg)
        # if is not cached
        if not cached:
            # we will download the file using our requests.Session
            response = self.get(sfile.url, stream=False)
            # if we don't have a 200 reponse we will return False
            if response.status_code != 200:
                log.error("Error: %s %s", response.status_code, response.reason)
                return False
            # we are not using it actually, anyway we should.
            sfile.content_type = response.headers['Content-Type']
            # let's write the file content.
            with open(sfile.filename, 'wb') as dfile:
                dfile.write(response.content)
        else:
            # if is cached just return True.
            log.info("... i'll use the cached one")
        return True

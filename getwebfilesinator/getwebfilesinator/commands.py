# -*- coding: utf-8 -*-
"""
===========================================
Commands :core:`getwebfilesinator.commands`
===========================================
Commands for the GetWebFilesInator
"""
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args
from getwebfilesinator.client import GwfiClient
from getwebfilesinator.utils import update_paths, getLogger
log = getLogger(__name__)

# Tell to ArgParseInator the class must be parsed for GetWebFilesInator
# commands and it is a ArgParseInated subclass.
@class_args
class Commands(ArgParseInated):
    """Commands for getwebfilesinator"""

    # we will check for the configuration file. Is a mandatory.
    def __preinator__(self):
        if not self.args.config:
            # if we don't have a configuration file we will exit using
            # the builtin __argpi__ (ArgParseInator Instance)
            __argpi__.exit(1, u'The configuration file is mandatory\n')

    # this will be the only command.
    @arg()
    def download(self):
        """Downloads files according with configuration"""
        # lets instantiate the client passing the configuration
        cli = GwfiClient(self.cfg)
        # now the client should process all the files
        # (should we change the name ?)
        cli.process(self.cfg.files or [])

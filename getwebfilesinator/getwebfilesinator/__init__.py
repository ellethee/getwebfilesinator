# -*- coding: utf-8 -*-
"""
=================
GetWebFilesInator
=================
GetWebFilesInator __init__ using ArgParseInator
"""
__version__ = "0.0.1"
from argparseinator import ArgParseInator
# import the commands module
import getwebfilesinator.commands
# import the config_factory form utils
from getwebfilesinator.utils import config_factory

# Instantiate an ArgParseInator Singleton telling we can handle configuration
# files using the config_factory.
ArgParseInator(config=(None, config_factory))

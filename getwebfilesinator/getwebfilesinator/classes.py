# -*- coding: utf-8 -*-
"""
========================================
Classes :mod:`getwebfilesinator.classes`
========================================
Classes for GetWebFilesInator
"""
from os.path import relpath
import re

class Singleton(type):
    """
    Singleton class.
    """
    _instances = {}
    __reinit__ = False

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Edo(dict):
    """
        Silly dict based class just to use the attribute syntax and Return
        None when items do not exists.
    """

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        if name in self.__dict__ or hasattr(self.__class__, name):
            super(Edo, self).__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            pass

    def __dir__(self):
        return self.keys() + self.__dict__.keys()

    def weakupdate(self, dtc, skipkeys=None):
        """Update value if key not exists and if non in _skipkeys"""
        skipkeys = skipkeys or []
        for key, value in dtc.iteritems():
            if not key in skipkeys and not key in self:
                self[key] = value

    @classmethod
    def dict2edo(cls, dtc):
        """
        Recursively convert dict to Edo objects.
        """
        if isinstance(dtc, list):
            for i, item in enumerate(dtc):
                dtc[i] = cls.dict2edo(item)
        if isinstance(dtc, tuple):
            dtc = list(dtc)
            for i, item in enumerate(dtc):
                dtc[i] = cls.dict2edo(item)
        elif isinstance(dtc, dict):
            for key, value in dtc.items():
                dtc[key] = cls.dict2edo(value)
        if isinstance(dtc, dict) and not isinstance(dtc, cls):
            return cls(dtc)
        return dtc

class ListKeeper(object):
    """Singleton class to keep targets list"""
    __metaclass__ = Singleton

    def __init__(self, cfg=None):
        self.cfg = cfg
        self.paths = cfg.paths
        self.targets = []

    @staticmethod
    def _is_intest(pattern, target):
        if not pattern:
            return True
        return re.search(pattern[1], target.get(pattern[0]) or '') is not None

    def get_from_path(self, path, pattern=None):
        """Return list of targets from path"""
        # first get all targets matching path and pattern if any.
        targets = [
            t for t in self.targets
            if t.target.startswith(path) and self._is_intest(pattern, t)]
        # then remove all filtered targets from the class targets.
        for target in targets:
            self.targets.remove(target)
        return targets

    def append(self, target):
        """Append target to targets list"""
        # remove the *static* part of the target.
        target.target = relpath(target.target, start=self.paths.static)
        # if target is a dict instance and have a index item we
        # use it to insert the target in the list
        if  isinstance(target.index, int):
            self.targets.insert(target.index, target)
        else:
            # else just append it.
            self.targets.append(target)

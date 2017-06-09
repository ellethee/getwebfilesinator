# -*- coding: utf-8 -*-
"""
====================================
Utils :mod:`getwebfilesinator.utils`
====================================
GetWebFilesInator utils.
"""
import os
from os.path import (
    join, basename, dirname, splitext, isfile, expanduser, expandvars, abspath)
from shlex import split
import fnmatch
import logging
import logging.config
from logging import getLogger
import re
import shutil
import sys
import zipfile
import json
import yaml
from getwebfilesinator import classes
GWFI_PATH = dirname(dirname(abspath(__file__)))
# default cache path
CACHE_PATH = join(GWFI_PATH, '.cache')
# default source block
BLOCKS = {
    'js': '<script type="text/javascript" src="{}"></script>',
    'css': '<link rel="stylesheet" href="{}">'
}
# githug checker
is_github = re.compile(r'(?!^https?:\/\/)^.+\/.+?$').search
# dowload checker
is_download = re.compile(r'^https?:\/\/.+\/.+\.\w+').search
# block parsing
parse_blocks = re.compile(
    r'(?ism)<!--\s*gwfi_block_(\w+)\s+(.+?)\s*-->').findall
# http deleter
del_http = re.compile(r'(?i)^https?:\/\/').sub
get_pattern = re.compile(r'\.(\w+)::(.+)?').match


def setup_logger():
    """Logger setup"""
    # get the log path
    logname = join(GWFI_PATH, 'getwebfilesinator.log')
    try:
        # try to get the logging configuration.
        logcfg = yaml.load(open(join(GWFI_PATH, 'logging.yaml'), 'rb'))
        # setup the FileHandler filename
        logcfg['handlers']['file']['filename'] = logname
        # load configuration via dictConfig
        logging.config.dictConfig(logcfg)
    except StandardError:
        # if some error nothing to do. standard logger
        pass
# setup the logger
setup_logger()
# get the logger for module.
log = getLogger(__name__)


def config_factory(filename):
    """The configuration factory"""
    ext = splitext(filename)[1].lower()
    try:
        # if is a yaml file.
        if ext in ['.yaml', '.yml']:
            # try to load configuration from yaml
            cfg = yaml.load(open(filename, 'rb'))
        # else if is a json
        elif ext == '.json':
            # try to load from json.
            cfg = json.load(filename)
        else:
            # if is a uknown file raise an Exception
            raise IOError('Unknow config type')
    except StandardError as error:
        # ok in this case we will log the error... it's just a basic
        # config_factory.
        log.exception(error)
        raise
    # if all is ok we will return a recursive Edo Object ('couse i'm too lazy
    # to use dictionaries in the *getitem* form.
    cfg['paths']['cfgpath'] = dirname(abspath(filename))
    return classes.Edo.dict2edo(cfg)



def mkdir(path):
    """Silly wrapper"""
    try:
        os.makedirs(path)
    except OSError:
        pass

def get_tree(path):
    """Silly linux-like tree"""
    text = ""
    # walk through path
    for root, _, files in os.walk(path):
        # set the level using the path separations.
        level = root.replace(path, '').count(os.sep)
        # calculate the indent
        indent = ' ' * 4 * (level)
        # set the text with relative indent
        text += '{}{}/\n'.format(indent, basename(root))
        # subindent ...
        subindent = ' ' * 4 * (level + 1)
        # add the *subfiles*
        for fpath in files:
            text += '{}{}\n'.format(subindent, fpath)
    return text

def update_paths(paths, dtc):
    """Updates paths"""
    # if dtc is a dict
    if isinstance(dtc, dict):
        # we will call upda recursively for every value in the dict
        for key, value in dtc.iteritems():
            dtc[key] = update_paths(paths, value)
    # if dtc is a list
    elif isinstance(dtc, list):
        # we will call upda recursively for every element in the list
        for idx, item in enumerate(dtc):
            dtc[idx] = update_paths(paths, item)
    # if dtc is a basestring
    elif isinstance(dtc, basestring):
        # we will try to format it using the *paths* dict
        try:
            dtc = expanduser(expandvars(dtc)).format(**paths)
        except IndexError:
            pass
    return dtc

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    ... copied from stackoverflow but i can't find the arcile now.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', unicode(value)).encode('ascii', 'ignore')
    value = unicode(re.sub(r'[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub(r'[-\s]+', '-', value))
    return value

def is_cached(sfile, cfg):
    """Check if dowload url is cached"""
    # comopse the filename for url relative to the cache path.
    filename = join(cfg.cache_path or CACHE_PATH, del_http('', sfile.url))
    # if we have some get querystring it better to slugify the querystring
    # part.
    if '?' in filename:
        parts = filename.split('?', 1)
        filename = join(parts[0] + slugify(parts[1]), sfile.filename)
    try:
        # if the file exist in the cache path and is not a **master.zip**
        # we will use the cached file.
        if isfile(filename) and basename(filename).lower() != 'master.zip':
            # we return the file is cached and te filename.
            return True, filename
    except IOError:
        pass
    # if the file doesn't exists or we have some error we will create the
    # folder.
    mkdir(dirname(filename))
    # and return that file is not cached with the filename.
    return False, filename


def zipglob(sfiles, namelist, path):
    """Returns a subset of filtered namelist"""
    files = []
    # cycle the sfiles
    for sfile in sfiles:
        # we will create a list of existing files in the zip filtering them
        # by the sfile filename
        sfile.zfiles = fnmatch.filter(namelist, join(path, sfile.filename))
        files += sfile.zfiles
    return files


def process_zip(sfile, cfg):
    """Process a zip file"""
    if not sfile.files:
        return
    with zipfile.ZipFile(sfile.filename, 'r') as zfile:
        # get the listname of zipped files
        lst = zfile.namelist()
        # we get the first name in list. if it is a folder it should be the
        # unzip root.
        first = lst[0]
        # comunque imposto la path iniziale al nome dello zip senza estensione.
        # Start analyzing path from the zip filename.
        path = splitext(basename(zfile.filename))[0]
        # Se il primo file in lista non comincia con il nome della path
        # *pronosticata* allora provo altre strade.
        # Il the first file in the list doesn't starts with the predicted path
        # then i'll try other paths.
        if not first.startswith(path):
            # try to set the path to first filename in the list, if it ends
            # with a '/' (it's a folder). Else we will set the path to an empty
            # string.
            path = first if first.endswith('/') else ''
            if path:
                # if we have a path we will check if all of our files exists in
                # the zip (omitting the wildcards filenames (for now).
                files = [
                    join(path, f.filename) for f in sfile.files
                    if not '*' in f.filename]
                # ok now we have the list, lets check with the filenames in the
                # archive.
                if not all([f in lst for f in files]):
                    # at this point if we don't have all the filenames
                    # corresponding we will set the path to an empty string.
                    # so all the next joins will be relative to the tmp path.
                    path = ''
        # At this point our path sould be right.
        # if is not we need some configuration agjustment.
        files = zipglob(sfile.files, lst, path)
        # if we don't have files will rise a Error
        if not files:
            raise KeyError("No corresponding files in archive")
        # extract all the filtered files
        zfile.extractall(sfile.tmpdir, files)
        # the ListKeeper Singleton instance.
        lstk = classes.ListKeeper()
        # cycle through the files in sfile
        for rfile in sfile.files:
            # copy parent's properties
            rfile.weakupdate(sfile, _skipkeys=['files'])
            # cycle through the extracted file for the rfile (could be a glob
            # syntax in the filename).
            for filename in [join(sfile.tmpdir, f) for f in rfile.zfiles]:
                # our target is a rfile copy with some difference.
                target = classes.Edo(rfile.copy())
                target.filename = filename
                # if we don't have a destination will try to guess it.
                target.dest = target.dest or guess_dest(filename, cfg)
                # at this point if we don't have a destination will raise an
                # Error.
                if not target.dest:
                    raise IOError("Can't find a destination for %s" % filename)
                # try to create the destination path
                mkdir(target.dest)
                # our target name
                target.target = join(target.dest, basename(filename))
                log.debug("Copying %s to %s", filename, target.target)
                # copy the file
                shutil.copy(filename, target.target)
                # append the target to the ListKeeper
                lstk.append(target)


def process_plain(sfile, cfg):
    """Copy a single file"""
    # try to guess the destination if we don't have one.
    if not sfile.dest:
        sfile.dest = guess_dest(sfile.filename, cfg)
    # at this point if we don't have a destination will raise an Error.
    if not sfile.dest:
        raise IOError("Can't find a destination for %s" % sfile.filename)
    # try to create the destination path
    mkdir(sfile.dest)
    # our target
    sfile.target = join(sfile.dest, basename(sfile.rename or sfile.filename))
    log.debug("Copying %s to %s", sfile.filename, sfile.target)
    # copy the file
    shutil.copy(sfile.filename, sfile.target)
    # the ListKeeper Singleton instance
    lstk = classes.ListKeeper()
    # append the sfile to the ListKeeper.
    lstk.append(sfile)


def guess_dest(filename, cfg):
    """Try to guess the destination"""
    # try to cycle through configured tests
    for test, dest in cfg.tests or []:
        # return the destination if matched
        if re.search(test, filename):
            return dest
    # else try to get the destination from the paths mapping using the
    # extension as key.
    return cfg.paths.get(splitext(filename.lower())[1][1:])


def get_blocks(text):
    """Get template blocks from the template"""
    # uses zip to create a list of dict(Edo) assign the keys to the resulted
    # match groups.
    blocks = [
        classes.Edo(zip(
            ['type', 'path', 'originalpattern'],
            [b[0].lower()] + split(b[1]) + ['']))
        for b in parse_blocks(text)]
    return blocks


def write_html(cfg):
    """Writes the html using the templates"""
    # static path for the relative urls
    static = join('/', basename(cfg.paths.static))
    # ListKeeper Singleton instance
    lstk = classes.ListKeeper()
    # list of blocks
    block_idx = []
    # cycle through the templates
    for template in cfg.templates:
        # get the template blocks.
        with open(template.source, 'rb') as fobj:
            template.blocks = get_blocks(fobj.read())
        # for each block will get the block template using the block type.
        for block in template.blocks:
            block.block = BLOCKS.get(block.type)
            block.template = template
            block.pattern = block.originalpattern
            pieces = get_pattern(block.pattern)
            if pieces:
                block.pattern = pieces.groups()
            elif block.pattern:
                block.pattern = ('target', block.pattern)
            # we use the block path lenght to insert the block in the list.
            # at the right position.
            if block.path:
                block_idx.append(block)
    # ok, sort reversed. Is better if we start to process from the longest path
    # plus pattern.
    block_idx.sort(key=lambda x: len(x.path + x.originalpattern), reverse=True)
    # cycle through our sorted blocks
    for block in block_idx:
        log.debug("Writing block %s", block.path)
        # load the template content if needed
        if not block.template.content:
            with open(block.template.source, 'rb') as fobj:
                block.template.content = fobj.read()
        # create the string block joining the formatted template block
        # for each target in the ListKeeper which starts with block path.
        sblock = "\n".join([
            block.block.format(join(static, t.target))
            for t in lstk.get_from_path(block.path, block.pattern)])
        # add some comment tag
        sblock = "\n".join([
            "<!-- gwfi {} {} -->".format(block.path, block.originalpattern),
            sblock,
            "<!-- /gwfi {} {} -->".format(block.path, block.originalpattern),
        ])
        # replace the template block with che string block.
        block.template.content = re.sub(
            r'(?ism)<!--\s*gwfi_block_{}\s+{}\s*{}\s*-->'.format(
                block.type, block.path, block.originalpattern),
            sblock, block.template.content)
    # Write templates result to the respective destinations.
    for template in cfg.templates:
        log.debug("Writing template %s", template.dest)
        mkdir(dirname(template.dest))
        with open(template.dest, 'wb') as fobj:
            fobj.write(template.content)

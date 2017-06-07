.. GetWebFilesInator documentation master file, created by
   sphinx-quickstart on Tue Jun  6 12:22:45 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GetWebFilesInator
=================
GetWebFilesInator (gwfi) is a simple file downloader to keep your javascript
and css libraries up to date. Is not perfect but is easily configurable and
for simplest tasks can be more suitable than a real dependency manager.

All you need is to know were your libraries are and a yaml o json configuration
file.

Requirements
------------

    - ArgParseInator    (pip install ArgParseInator)
    - PyYAML            (pip install PyYAML)
    - requests          (pip install requests)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   configuration/index
   downloaders/index

.. note::
    I made this script for a personal need is not intended for professional use.

.. todo::
    Implement middlewares.

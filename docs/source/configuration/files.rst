Files
-----
Files section in where we define what to download which files will be copied and so on...

A file element can have many attribute it depends on what you want to do and on what downloader will be used.

Attributes for default downloaders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For the defaults downloaders (download, local and github related) theses are the attributes.

  - get_type: which downloader need to get this file
  - url:  where to download the file/lib/zip the downloaders can use this to guess what kind of get_type if not specified.
  - filename: the filename can be used with url to guess the get_type if not specified.
  - rename: rename the file.
  - name: to filter (in case of github get_type) 
  - filter: a regex to filter (in case of github get_type) 
  - dest: destination for the file or files.
  - files: list of sub files to process
      - filename: name of the file.
      - dest: destination for the file

Examples
^^^^^^^^
For theses examples i assume we have a configuration like this to avoid problems
with paths to guess destination:

.. code-block:: yaml

  paths:
    static: "~/src/django-site/static"
    js: "{static}/js"
    css: "{static}/css"
    fonts: "{static}/fonts"

  tests:
    - ['(?i)\.js$', "{js}"]
    - ['(?i)\.css$', "{css}"]
    - ['(?i)\.(woff2?|ttf|otf|eot)$', "{fonts}"]


Local file
""""""""""
Just copy a local file.

.. code-block:: yaml
  
  files:
    - filename: "~/src/js/palette.js"

Single file download
""""""""""""""""""""
Directly download a single file from url and copy it as is.
We define only the *comlplete* url the get_type and the action to take
is guessed by the downloaders.

.. code-block:: yaml
  
  files:
    - url: https://code.jquery.com/jquery-3.2.1.min.js

Single file download with get query string
""""""""""""""""""""""""""""""""""""""""""
Passing the query string to the url and use the filename to tell how to save the result.

.. code-block:: yaml
  
  files:
    - url: https://sciactive.com/pnotify/buildcustom.php?mode=js&min=true&modules=desktop-buttons-nonblock-animate-confirm-callbacks-history&cff=.js
      filename: pnotify.custom.min.js

GitHub raw download
"""""""""""""""""""
Download a raw file from github.
We define *user/repository* as url and the filename of the file to download.

.. code-block:: yaml

  files:
    - url: moment/moment
      filename: min/moment-with-locales.min.js

GitHub latest release
"""""""""""""""""""""
Try to get latest release or the master.zip if can't valid assets.
We define *user/repository* as url and use the *files* list to tell which files 
to download.

.. code-block:: yaml

  - url: 'twbs/bootstrap'
    files:
      - filename: js/bootstrap.min.js
      - filename: css/bootstrap.min.css
      - filename: css/bootstrap-theme.min.css
      - filename: fonts/*.woff*   # note we can use wildcards

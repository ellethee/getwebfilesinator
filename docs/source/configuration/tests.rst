Tests
-----
Simple tests definition, using regex, to guess the destination path when not specified.

It's a list of lists where the first element is the regex and the second is the destination path.

.. code-block:: yaml

    # define our tests using regex to guess destination for files.
    tests:
      # if the filename has locale or locales in his path the destination is {locales}
      - ['(?i)\/locales?\/.*\.js$', "{locales}"]  
      # if the filename ends with .js the destination is {js}
      - ['(?i)\.js$', "{js}"]
      # if the filename ends with .css the destination is {css}
      - ['(?i)\.css$', "{css}"]
      # if the filename ends with woff,woff2,otf,eot the destination is {fonts}
      - ['(?i)\.(woff2?|ttf|otf|eot)$', "{fonts}"]

.. note::

    If no destination is specified and all the tests files **gwfi** try to get 
    the path from extension. 

    For example if a I have a **testme.lib** file and I have mapped the path
    **lib: "{static}/js/lib"** the destination will be **{lib}**


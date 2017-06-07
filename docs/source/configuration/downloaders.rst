Downloaders
-----------
In this section you can define custom downloaders.

example:

.. code-block:: yaml

    # paths mapping
    paths:
      source: "~/src/django-site/"
      static: "{source}/static"
      downloaders: "~/src/python/gwfi_downloaders"

    # add a custom downloader.
    downloaders:
      - [test_downloader, "{downloaders}/test_downloader.py"]

.. note::
    see `Custom Downloaders`_

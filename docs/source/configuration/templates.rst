Templates
---------
You can define a list of templates which will be use to create html files with links
to the relative static path for files.

The gwfi template block syntax is very simple

**gwfi_block_{type} {path} [[.property::]{pattern}]**

    - type - the :ref:`SourceBlocks` mapping key
    - path - the path, relative to the {static} reference (see :ref:`Paths`)
    - pattern - optional regex for granular filtering.

As you can see the pattern can be write in simple and complex way.

  - simple: just the regex pattern it will be used to filter the **target** property (filename complete with destination path)
  - complex: the property name and the regex pattern wrote in the form **.property_name::pattern**

.. code-block:: html
    :linenos:
    :emphasize-lines: 2,3

    <!-- Core Scripts - Include with every page -->
    <!-- gwfi_block_js js jquery -->
    <!-- gwfi_block_js js .group::django-->
    <!-- gwfi_block_js js -->
    <!-- gwfi_block_js js/locales -->
    <!-- gwfi_block_css css -->

In the example above in **line 2** we filter all the filenames that contains ``jquery``
and in the **line 3** we filter all the items that have the property ``group`` which contains ``django``.

Will generate this html file

.. code-block:: html
    :linenos:

    <!-- Core Scripts - Include with every page -->
    <!-- gwfi js jquery -->
    <script type="text/javascript" src="/static/js/jquery-3.2.1.min.js"></script>
    <!-- /gwfi js jquery -->
    <!-- gwfi js  -->
    <script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="/static/js/pnotify.custom.min.js"></script>
    <!-- /gwfi js  -->
    <!-- gwfi js/locales  -->

    <!-- /gwfi js/locales  -->
    <!-- gwfi js .group::django -->
    <script type="text/javascript" src="/static/js/fullcalendar.min.js"></script>
    <script type="text/javascript" src="/static/js/locales/fullcalendar/it.js"></script>
    <script type="text/javascript" src="/static/js/moment-with-locales.min.js"></script>
    <!-- /gwfi js .group::django -->
    <!-- gwfi css  -->
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/fullcalendar.min.css">
    <link rel="stylesheet" href="/static/css/pnotify.custom.min.css">
    <!-- /gwfi css  -->

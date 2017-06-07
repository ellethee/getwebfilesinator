.. _Paths:

Paths
-----
In the paths section you can define all the destinations path for the downloaded files.
The values will be expanded so you can use environment vars and references to other paths.

example:

.. code-block:: yaml

    paths:
      source: "~/src/django-site/"
      static: "{source}/static"
      js: "{static}/js"
      css: "{static}/css"

will be expanded to

.. code-block:: yaml
   
    paths:
        source: "/home/username/src/django"
        static: "/home/username/src/django/static"
        js: "/home/username/src/django/static/js"
        css: "/home/username/src/django/static/css"

.. NOTE::
    - The **static** path must be present in the paths mapping.
    - You can use the **{gwfi}** in paths to refer to the script path.


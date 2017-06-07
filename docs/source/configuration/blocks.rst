.. _SourceBlocks:

Source Blocks
-------------
The source block are the part of html that will be inserted in the template for each file

The default source blocks are:

.. code-block:: html

    <!-- for js files -->
    <script type="text/javascript" src="{}"></script>

    <!-- for css files -->
    <link rel="stylesheet" href="{}">


you can map your source block with the extension name and the block text

.. code-block:: yaml

    blocks:
      img: '<img src="{}" alt="void">'

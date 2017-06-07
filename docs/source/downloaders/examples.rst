Examples
--------

Moaning downloader
^^^^^^^^^^^^^^^^^^
A silly example which do nothing, except to moan for his poor situation.

.. code-block:: python

    from logging import getLogger
    from getwebfilesinator.downloaders.downloaders_defaults import Downloader
    log = getLogger(__name__)

    class DownloaderTest(Downloader):
        """Test downloader"""

        # Our get type so we can map the Downloader
        get_type = 'test_download'
        # Actually we don't need a guess_priority in this case, we cant omit this

        def download(self, sfile):
            """Download the file"""
            # just log something..
            log.info(":'( I'm a test downloader. No actions for me :'(")
            # and return False so the file will not be processed
            return False

        def guess_type(self, sfile):
            """Guess retrieve type"""
            # just verify is the url is 'imatest'
            if sfile.url == 'imatest':
                return self

Greet (action included)
^^^^^^^^^^^^^^^^^^^^^^^
This silly downloader uses a personal action to bypass the standard client
behavior.

.. code-block:: python

    from logging import getLogger
    from getwebfilesinator.downloaders.downloaders_defaults import Downloader
    log = getLogger(__name__)

    class DownloaderGreet(Downloader):
        """
        Downloader with action included

        our url must start with greet://
        """

        get_type = 'greet'

        def guess_type(self, sfile):
            """Guess the type"""
            # the url must starts with ``greet://``
            if sfile.url.startswith('greet://'):
                return self

        def download(self, sfile):
            """Process sfile"""
            # OK retrieve our greet part.
            sfile.greet = sfile.url[8:]
            # and return our action, this will be executed by the client.
            return self.greet

        def greet(self, sfile, cfg):
            """ Greeting action """
            # just greet.
            log.info("Now we are greeting %s", sfile.greet)


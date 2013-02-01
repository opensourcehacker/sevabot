============================================================
Sending Skype messages from Python
============================================================

.. contents:: :local:

Introduction
===============

Here is an example how to send messages to Skype chat from external Python scripts and services.
They do not need to be Sevabot commands, messages are send over HTTP interface.

Sending messages from separate URL thread
============================================================

Here is an example (`orignal code <https://github.com/miohtama/collective.logbook/blob/master/collective/logbook/browser/webhook.py#L49>`) how to
send a message asynchronously (does not executing the orignal code).

Example::

    import socket
    import threading
    import urllib
    import urllib2
    import logging

    logger = logging.getLogger(__name__) # Write errors to PYthon logging output

    # Seconds of web service timeout
    WEBHOOK_HTTP_TIMEOUT = 30

    # Get Skype chat id from Sevabot web inteface
    CHAT_ID = "xxx"

    class UrlThread(threading.Thread):
        """
    A separate thread doing HTTP POST so we won't block when calling the webhook.
    """
        def __init__(self, url, data):
            threading.Thread.__init__(self)
            self.url = url
            self.data = data

        def run(self):
            orignal_timeout = socket.getdefaulttimeout()
            try:
                self.data = urllib.urlencode(self.data)
                socket.setdefaulttimeout(WEBHOOK_HTTP_TIMEOUT)
                r = urllib2.urlopen(self.url, self.data)
                r.read()
            except Exception as e:
                logger.error(e)
                logger.exception(e)
            finally:
                socket.setdefaulttimeout(orignal_timeout)

    message = "Hello world"
    t = UrlThread("http://sevabot.something.example.com:5000/message_unsigned/", {'message': message, 'chat_id': CHAT_ID})


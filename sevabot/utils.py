"""

    Helper functions

"""

import hashlib
import logging

logger = logging.getLogger("sevabot")


def ensure_unicode(value):
    """
    Make sure we have a valid unicode string.
    """

    if type(value) == str:
        # Ignore errors even if the string is not proper UTF-8 or has
        # broken marker bytes.
        # Python built-in function unicode() can do this.
        value = unicode(value, "utf-8", errors="ignore")
    else:
        # Assume the value object has proper __unicode__() method
        value = unicode(value)

    return value


def fail_safe(func):
    """
    Python decorator to make sure we don't let exceptions slip through.

    We log all exceptions to logging output.
    """

    def closure(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            return False

    return closure


def get_chat_id(chat):
    """
    Get unique internal persistent id of the chat object.

    All ids are URL safe.

    This is the same id as in the web interface.

    :param chat: Skype4Py.chat.Chat instance
    """
    m = hashlib.md5()
    m.update(chat.Name)
    return m.hexdigest()


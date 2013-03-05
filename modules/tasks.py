#!/sevabot
"""

    Simple group chat task manager.

    This also serves as an example how to write stateful handlers.

"""

import os
import logging
import tempfile
import pickle
from collections import OrderedDict

from sevabot.bot.stateful import StatefulHandler

logger = logging.getLogger("Tasks")

logger.debug("Tasks body level reload")


class TasksHandler(StatefulHandler):
    """
    Skype message handler class for the task manager.
    """

    def __init__(self):
        """Use `init` method to initialize a handler.
        """
        logger.debug("Tasks constructed")

    def init(self, skype):
        """
        Set-up our state. This is called

        :param skype: Handle to Skype4Py instance
        """
        logger.debug("Tasks init")
        self.skype = skype
        self.status_file = os.path.join(tempfile.gettempdir(), "sevabot-tasks.pickle")
        self.status = Status.load(self.status_file)

    def save(self):
        """
        Persistent our state.
        """
        Status.write(self.status_file, self.status)

    def handle_message(self, msg, status):
        """Override this method to customize a handler.
        """
        logger.debug("Tasks handler got:" % msg.encode("utf-8"))

    def shutdown():
        """ Called when the module is reloaded.

        ..note ::

             We do *not* guaranteed to be call when Sevabot process shutdowns.
        """
    logger.debug("Tasks handler shutdown")


class Status:
    """
    Stored pickled state of the tasks.

    Use Python pickling serialization for making status info persistent.
    """

    def __init__(self):
        # Skype username -> Task instance mappings
        self.tasks = OrderedDict()

    @classmethod
    def read(cls, path):
        """
        Read status file.

        Return fresh status if file does not exist.
        """

        if not os.path.exists(path):
            # Status file do not exist, get default status
            return Status()

        f = open(path, "rb")

        try:
            return pickle.load(f)
        finally:
            f.close()

    @classmethod
    def write(cls, path, status):
        """
        Write status file
        """
        f = open(path, "wb")
        pickle.dump(status, f)
        f.close()


class Job:
    """
    Tracks who is doing what
    """

    def __init__(self, real_name, started, task):
        """
        :param started: datetime when the job was started
        """
        self.started = started
        self.task = task
        self.real_name = real_name


# Export the instance to Sevabot
sevabot_handler = TasksHandler()

__all__ = ["sevabot_handler"]

"""

    Stateful module base class and interface description.

"""


class StatefulHandler:
    """
    Base class for stateful handlers.

    All exceptions slip through are caught and logged.
    """

    def init(self, skype):
        """
        Set-up our state. This is called every time module is (re)loaded.

        :param skype: Handle to Skype4Py instance
        """

    def handle_message(self, msg, status):
        """Override this method to have a customized handler for each Skype message.
        """

    def shutdown():
        """ Called when the module is reloaded.

        ..note ::

             We do *not* guaranteed to be call when Sevabot process shutdowns as
             the process may terminate with SIGKILL.

        """

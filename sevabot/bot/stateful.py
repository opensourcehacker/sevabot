"""

    Stateful module base class and interface description.

    All stateful Python modules

    - Get Skype4Py Skype instance on init - have full control over Skype and
      thus are not limited to !command handlers

    - Reside in the some modules/ folder as UNIX script modules

    - Have .py extension and be valid Python 2.7 modules

    - Have #!/sevabot magic string at the head of the file

    - Exports Python attribute *sevabot_handler* which is an instance of the class
      as described below

    Please note that in the future we might have different chat backends (GTalk)
    and thus have a same-same-but-different stateful handlers.

"""


class StatefulSkypeHandler:
    """
    Base class for stateful handlers.

    All exceptions slip through are caught and logged.
    """

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        You can get Skype4Py instance via ``sevabot.getSkype()``.

        :param sevabot: Handle to Sevabot instance
        """

    def handle_message(self, msg, status):
        """Override this method to have a customized handler for each Skype message.

        :param msg: ChatMessage instance https://github.com/awahlig/skype4py/blob/master/Skype4Py/chat.py#L409

        :param status: -

        :return: True if the message was handled and should not be further processed
        """

    def shutdown():
        """ Called when the module is reloaded.

        In ``shutdown()`` you must

        * Stop all created threads

        * Unregister all event handlers

        ..note ::

             We do *not* guaranteed to be call when Sevabot process shutdowns as
             the process may terminate with SIGKILL.

        """

    def register_callback(self, skype, event, callback):
        """
        Register any callable as a callback for a skype event.

        Thin wrapper for RegisterEventHandler https://github.com/awahlig/skype4py/blob/master/Skype4Py/utils.py

        :param skype: Skype4Py instance

        :param event: Same as Event

        :param callback: Same as Target

        :return: Same as RegisterEventHandler
        """

        return skype.RegisterEventHandler(event, callback)

    def unregister_callback(self, skype, event, callback):
        """
        Unregister a callback previously registered with register_callback.

        Thin wrapper for UnregisterEventHandler https://github.com/awahlig/skype4py/blob/master/Skype4Py/utils.py

        :param skype: Skype4Py instance

        :param event: Same as Event

        :param callback: Same as Target

        :return: Same as UnregisterEventHandler
        """

        return skype.UnregisterEventHandler(event, callback)

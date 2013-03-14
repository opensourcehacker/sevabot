#!/sevabot

# -*- coding: utf-8 -*-

"""
Simple conference call hosting
"""
from __future__ import unicode_literals

import logging
import Skype4Py

from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode

logger = logging.getLogger('Call')

# Set to debug only during dev
logger.setLevel(logging.INFO)

logger.debug('Call module level load import')

HELP_TEXT = """Simple conference call hosting allows you to have bot host a conference call from the chat.

Sevabot can have only one conference call at the same instance.

Commands:

!call help: Show this help text

!call: Start a conference call from the chat

!call start: Same as !call

!call end: Finish the conference call from the chat
"""


class CallHandler(StatefulSkypeHandler):

    """
    Skype message handler class for the conference call hosting.
    """

    def __init__(self):
        """
        Use `init` method to initialize a handler.
        """

        logger.debug('Call handler constructed')

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        :param skype: Handle to Skype4Py instance
        """

        logger.debug('Call handler init')

        self.skype = sevabot.getSkype()
        self.calls = {}

        self.commands = {'help': self.help, 'start': self.start_call, 'end': self.end_call}

    def handle_message(self, msg, status):
        """
        Override this method to customize a handler.
        """

        body = ensure_unicode(msg.Body)

        logger.debug('Call handler got: {}'.format(body))

        # If the separators are not specified, runs of consecutive
        # whitespace are regarded as a single separator
        words = body.split()

        if not len(words):
            return False

        if words[0] != '!call':
            return False

        args = words[1:]

        if not len(args):
            # !call simply starts a call
            self.start_call(msg, status, args)
            return True

        for name, cmd in self.commands.items():
            if name == args[0]:
                cmd(msg, status, args)
                return True

        return False

    def shutdown():
        """
        Called when the module is reloaded.
        """
        logger.debug('Call handler shutdown')

    def help(self, msg, status, args):
        """
        Show help message to the sender.
        """
        msg.Chat.SendMessage(HELP_TEXT)

    def is_call_active(self, chat_name=None):
        """
        Is a call from the chat active?
        """

        if not chat_name:
            # Is any call active?
            return len(self.skype.ActiveCalls) > 0

        call = self.calls.get(chat_name, False)

        if not call:
            # Calls from the chat are not active
            return False

        conference_id = call.ConferenceId

        if conference_id > 0:
            conference = self.skype.Conference(conference_id)
            return len(conference.ActiveCalls) > 0
        else:
            return call.Status == Skype4Py.clsOnHold or call.Status == Skype4Py.clsLocalHold or call.Status == Skype4Py.clsRemoteHold or call.Status == Skype4Py.clsInProgress

    def start_call(self, msg, status, args):
        """
        Start a conference call of the chat if any call is not active.
        """

        chat_name = msg.Chat.Name

        if self.is_call_active():
            # Already active
            if not self.is_call_active(chat_name):
                msg.Chat.SendMessage('Sorry, I\'m talking with someone else...')
            return

        def callback(call, status):
            logger.debug('Call status changed (wait): {} - {} - {}'.format(call.Id, call.Status, call.PartnerHandle))

            if status in (Skype4Py.clsRinging, Skype4Py.clsInProgress):
                self.calls[chat_name] = call
                self.unregister_callback(self.skype, 'CallStatus', callback)

        success = self.register_callback(self.skype, 'CallStatus', callback)
        if not success:
            logger.debug('CALL already issued on {}'.format(chat_name))
            return

        # Dirty workaround to start a conference call from a chat
        call_command = self.skype.Command('CALL {}'.format(chat_name))
        self.skype.SendCommand(call_command)

    def end_call(self, msg, status, args):
        """
        Finish a conference call of the chat.
        """

        chat_name = msg.Chat.Name

        if not self.is_call_active(chat_name):
            # No active calls
            msg.Chat.SendMessage('No calls to finish.')
            return

        call = self.calls.get(chat_name, False)
        if not call:
            # Should be never reached
            return

        conference_id = call.ConferenceId
        if conference_id > 0:
            self.skype.Conference(conference_id).Finish()
        else:
            call.Finish()


# Export the instance to Sevabot
sevabot_handler = CallHandler()

__all__ = ['sevabot_handler']

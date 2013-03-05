# -*- coding: utf-8 -*-

"""
Message handler base class and a built-in command handler.

Each subclass of `HandlerBase` whose name ends with `Handler` is
instantiated and used as a message handler automatically.

To add a custom handler, put a definition of a class which inherits
`HandlerBase` in `custom_handlers.py`.
You can override these two methods to customize a handler:
    - init(self)
    - handle(self, msg, status)
"""
from __future__ import absolute_import, division, unicode_literals

import re
import logging
import Skype4Py
import shlex
from inspect import getmembers, ismethod

from sevabot.bot import modules

logger = logging.getLogger('sevabot')


class HandlerBase:

    """The base class for all handler classes.
    """

    def __init__(self, skype):
        """Use `init` method to initialize a handler.
        """

        self.skype = skype

    def init(self):
        """Override this method to initialize a handler.
        """

        pass

    def handle(self, msg, status):
        """Override this method to customize a handler.
        """

        pass


class CommandHandler(HandlerBase):
    """A handler for processing built-in or non built-in commands.
    """

    def init(self):
        self.calls = {}
        self.cache_builtins()
        self.set_event_handlers()

    def cache_builtins(self):
        """Scan all built-in commands defined in this handler.
        """

        def wanted(member):
            return ismethod(member) and member.__name__.startswith('builtin_')

        self.builtins = {}
        for member in getmembers(self, wanted):
            command_name = re.split('^builtin_', member[0])[1]
            self.builtins[command_name] = member[1]
            logger.info('Built-in command {} is available.'.format(command_name))

    def set_event_handlers(self):
        """Set Skype event handlers.
        """

        def callstatus_handler(call, status):
            logger.debug('Call status changed: {} - {} - {}'.format(call.Id, call.Status, call.PartnerHandle))

        self.skype.OnCallStatus = callstatus_handler

    def handle(self, msg, status):
        """Handle command messages.
        """

        body = msg.Body.encode('utf-8')

        # shlex dies on unicode on OSX with null bytes all over the string
        words = shlex.split(body, comments=False, posix=True)
        words = [word.decode('utf-8') for word in words]

        if len(words) < 1:
            return

        command_name = words[0]
        command_args = words[1:]

        # Check all stateful handlers
        for handler in modules.get_message_handlers():
            handler(msg, status)

        # Beyond this point we process script commands only
        if not command_name.startswith('!'):
            return

        command_name = command_name[1:]

        script_module = modules.get_script_module(command_name)

        if command_name in self.builtins:
            # Execute a built-in command
            logger.debug('Executing built-in command {}: {}'.format(command_name, command_args))
            self.builtins[command_name](command_args, msg, status)
        elif script_module:

            # Execute a module asynchronously
            def callback(output):
                msg.Chat.SendMessage(output)

            script_module.run(command_name, command_args, callback)
        else:
            msg.Chat.SendMessage("Don't know about command: !" + command_name)

    def builtin_reload(self, args, msg, status):
        """Reload command modules.
        """

        commands = modules.load_modules()
        msg.Chat.SendMessage('Available commands: %s' % ', '.join(commands))

    def is_call_active(self, chat_name=None):
        """Return if a call from the chat is active.
        """

        if not chat_name:
            return len(self.skype.ActiveCalls) > 0

        call = self.calls.get(chat_name, False)
        if call:
            conf_id = call.ConferenceId
            if conf_id > 0:
                conf = self.skype.Conference(conf_id)
                return len(conf.ActiveCalls) > 0
            else:
                return call.Status == Skype4Py.clsOnHold or call.Status == Skype4Py.clsLocalHold or call.Status == Skype4Py.clsRemoteHold or call.Status == Skype4Py.clsInProgress
        else:
            return False

    def finish_calls(self, chat_name=None):
        """Finish all active calls from the chat.
        """

        if not chat_name:
            for call in self.skype.ActiveCalls:
                call.Finish()
            return

        call = self.calls.get(chat_name, False)
        if call:
            conf_id = call.ConferenceId
            if conf_id > 0:
                self.skype.Conference(conf_id).Finish()
            else:
                call.Finish()

    def hold_calls(self, chat_name=None):
        """Hold all active calls from the chat.
        """

        if not chat_name:
            for call in self.skype.ActiveCalls:
                call.Hold()
            return

        call = self.calls.get(chat_name, False)
        if call:
            conf_id = call.ConferenceId
            if conf_id > 0:
                self.skype.Conference(conf_id).Hold()
            else:
                call.Hold()

    def resume_calls(self, chat_name):
        """Resume all active calls from the chat."""

        call = self.calls.get(chat_name, False)
        if call:
            conf_id = call.ConferenceId
            if conf_id > 0:
                self.skype.Conference(conf_id).Resume()
            else:
                call.Resume()

    def builtin_call(self, args, msg, status):
        """Call a target or add a user to an existing call.
        """

        chat_name = msg.Chat.Name

        if len(args) < 1:

            if self.is_call_active():
                if not self.is_call_active(chat_name):
                    msg.Chat.SendMessage("Sorry, I'm talking with someone else...")
                return

            old_callback = self.skype.OnCallStatus

            def callback(call, status):
                logger.debug('Call status changed (wait): {} - {} - {}'.format(call.Id, call.Status, call.PartnerHandle))

                if status == Skype4Py.clsRinging or status == Skype4Py.clsInProgress:
                    self.calls[chat_name] = call
                    self.skype.OnCallStatus = old_callback

            call_command = self.skype.Command('CALL {}'.format(chat_name))
            self.skype.SendCommand(call_command)
            self.skype.OnCallStatus = callback

            return

        command = args[0]
        command_args = args[1:]

        if command == 'end':

            if self.is_call_active(chat_name):
                self.finish_calls(chat_name)
            else:
                msg.Chat.SendMessage('No calls to finish.')
        elif command == 'add':

            if not self.is_call_active(chat_name):
                msg.Chat.SendMessage('Try !call first.')
                return

            if len(command_args) < 1:
                msg.Chat.SendMessage("I don't know who you want to add.")
                return

            msg.Chat.SendMessage('Hey, Skype! Tell me how to do this!')
        else:

            # Workaround:
            #  Hold an existing call and call a user to add, then
            #  join the call with the original call.

            # self.hold_calls(chat_name)

            # name = command_args[0]
            # msg.Chat.SendMessage("Calling " + name + " ...")
            # temp_call = self.skype.PlaceCall(name)

            # msg.Chat.SendMessage("Joining calls...")
            # temp_call.Join(self.calls[chat_name])

            msg.Chat.SendMessage("Don't know command of call: " + command)

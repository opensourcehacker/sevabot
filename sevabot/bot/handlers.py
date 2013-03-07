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
from sevabot.utils import ensure_unicode

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

        # Check all stateful handlers
        for handler in modules.get_message_handlers():
            processed = handler(msg, status)
            if processed:
                # Handler processed the message
                return

        # We need utf-8 for shlex
        body = ensure_unicode(msg.Body).encode('utf-8')

        logger.debug(u"Processing message, body %s" % msg.Body)

        # shlex dies on unicode on OSX with null bytes all over the string
        try:
            words = shlex.split(body, comments=False, posix=True)
        except ValueError:
            # ValueError: No closing quotation
            return

        words = [word.decode('utf-8') for word in words]

        if len(words) < 1:
            return

        command_name = words[0]
        command_args = words[1:]

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

            script_module.run(msg, command_args, callback)
        else:
            msg.Chat.SendMessage("Don't know about command: !" + command_name)

    def builtin_reload(self, args, msg, status):
        """Reload command modules.
        """

        commands = modules.load_modules(self)
        msg.Chat.SendMessage('Available commands: %s' % ', '.join(commands))

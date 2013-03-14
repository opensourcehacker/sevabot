# -*- coding: utf-8 -*-

"""
Handler class for processing built-in commands and delegating messages.
"""
from __future__ import absolute_import, division, unicode_literals

import re
import logging
import shlex
from inspect import getmembers, ismethod

from sevabot.bot import modules
from sevabot.utils import ensure_unicode

logger = logging.getLogger('sevabot')


class CommandHandler:
    """A handler for processing built-in commands and delegating messages to reloadable modules.
    """

    def __init__(self, sevabot):
        self.sevabot = sevabot
        self.calls = {}
        self.cache_builtins()

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

    def handle(self, msg, status):
        """Handle command messages.
        """

        # If you are talking to yourself when testing
        # Ignore non-sent messages (you get both SENDING and SENT events)
        if status == "SENDING":
            return

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
        commands = modules.load_modules(self.sevabot)
        msg.Chat.SendMessage('Available commands: %s' % ', '.join(commands))

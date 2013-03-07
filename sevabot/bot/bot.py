# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import logging
import hashlib
import time
from collections import OrderedDict
from inspect import getmembers, isclass

import Skype4Py

from sevabot.bot import handlers
from sevabot.utils import get_chat_id


logger = logging.getLogger("sevabot")


class Sevabot:
    """
    Skype bot interface handler.
    """

    def __init__(self):
        self.cmds = {}
        self.chats = {}
        self.handlers = {}

    def start(self):

        if sys.platform == "linux2":
            self.skype = Skype4Py.Skype(Transport='x11')
        else:
            # OSX
            self.skype = Skype4Py.Skype()

        logger.debug("Attaching to Skype")
        self.skype.Attach()

        logger.debug("Skype API connection established")
        self.skype.OnMessageStatus = self.handleMessages

        self.cacheChats()

        # XXX: Might need refactoring logic here how master handler is registered
        self.handler = handlers.CommandHandler(self)

    def getSkype(self):
        """ Expose Skype to stateful modules.

        :return: Active Skype4Py instance
        """
        return self.skype

    def cacheChats(self):
        """
        Scan all chats on initial connect.
        """
        logger.debug("Async cacheChats() -- this may take a while")
        self.chats = OrderedDict()

        # First get all fresh chats
        chats = []
        for chat in self.skype.Chats:

            # filter chats older than 6 months
            if time.time() - chat.ActivityTimestamp > 3600 * 24 * 180:
                continue

            chats.append(chat)

        chats = sorted(chats, key=lambda c: c.ActivityTimestamp, reverse=True)

        for chat in chats:
            # Encode ids in b64 so they are easier to pass in URLs
            chat_id = get_chat_id(chat)
            self.chats[chat_id] = chat

    def getOpenChats(self):
        """
        Get list of id -> chat object of all chats which are open.
        """

        # Make sure we get refresh chat list every time
        self.cacheChats()
        for chat_id, chat in self.chats.items():
            yield chat_id, chat

    def handleMessages(self, msg, status):
        """
        Handle incoming messages.
        """

        logger.debug("Incoming %s - %s - %s: %s" % (status, msg.Chat.FriendlyName,
                                                    msg.FromHandle, msg.Body))

        self.handler.handle(msg, status)

    def sendMessage(self, chat, msg):
        """
        Send a message to chat.

        :param chat: Chat id as a string

        :param msg: Message as UTF-8 encoded string
        """
        try:
            self.chats[chat].SendMessage(msg)
            return "Message sent\n"
        except KeyError:
            raise RuntimeError("No chat %s" % chat)

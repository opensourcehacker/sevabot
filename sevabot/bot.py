# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from glob import glob
import imp
import sys
import logging

import Skype4Py

from sevabot import modules

logger = logging.getLogger("sevabot")


class Sevabot:
    """
    Skype bot interface handler.
    """

    def __init__(self):
        self.cmds = {}
        self.cron = []
        self.chats = {}

    def start(self):

        if sys.platform == "Linux" or sys.platform == "linux" or sys.platform == "linux2":
            self.skype = Skype4Py.Skype(Transport='x11')
        else:
            # OSX
            self.skype = Skype4Py.Skype()

        self.skype.Attach()
        self.skype.OnMessageStatus = self.handleMessages

        self.getChats()

    def getChats(self):
        """
        Scan all chats on initial connect.
        """
        chats = {}
        for chat in self.skype.Chats:
            chats[chat.FriendlyName] = chat
        self.chats = chats

    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        """
        if status == "RECEIVED" or status == "SENT":
            logger.debug("%s - %s - %s: %s" % (status, msg.Chat.FriendlyName, msg.FromHandle, msg.Body))

        if status in ["RECEIVED", "SENT"] and msg.Body:

            words = msg.Body.split()

            if len(words) < 0:
                return

            keyword = words[0]

            if not keyword.startswith("!"):
                return

            keyword = keyword[1:]

            logger.debug("Trying to identify keyword: %s" % keyword)

            if keyword == "reload":
                commands = modules.load_modules()
                msg.Chat.SendMessage("Available commands: %s" % ", ".join(commands))
                return

            if modules.is_module(keyword):
                # Execute module asynchronously

                def callback(output):
                    msg.Chat.SendMessage(output)

                modules.run_module(keyword, words[1:], callback)
                return

            if msg.Body == "!loadModules":
                msg.Chat.SendMessage("Loading modules...")
                try:
                    self.loadModules()
                except Exception as e:
                    msg.Chat.SendMessage(str(e))
                    return
                return

            elif msg.Body == "!loadChats":
                self.getChats()
                return

    def runCmd(self, cmd):
        args = cmd.split(" ")
        return self.cmds["!" + args[0]](*args[1:], bot=self, skype=self.skype)

    def sendMsg(self, chat, msg):
        try:
            self.chats[chat].SendMessage(msg)
            return "Message sent\n"
        except KeyError as e:
            return "Chat not found\n"

    def runCron(self, interval):
        """
        Run cron jobs defined by modules.
        This function is called from the main script.
        Interval is the same as the main loops time.sleep's interval.
        """

        for job in self.cron:
            if 'timer' not in job:
                job['timer'] = job['interval']

            # get the chat objects for the cron job
            chats = []
            if type(job['chats'][0]) == str:
                for chat in job['chats']:
                    try:
                        chat = self.chats[chat]
                        chats.append(chat)
                    except KeyError:
                        pass
                job['chats'] = chats

            job['timer'] -= interval

            if job['timer'] <= 0:
                try:
                    job['cmd'](chats=job['chats'])
                except Exception as e:
                    print("Error " + str(e))
                job['timer'] = job['interval']

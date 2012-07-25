# -*- coding: utf-8 -*-

from glob import glob
import imp

import Skype4Py


class Sevabot:
    def __init__(self):
        self.cmds = {}
        self.cron = []
        self.chats = {}
        self.loadModules()

        self.skype = Skype4Py.Skype(Transport='x11')
        self.skype.Attach()
        self.skype.OnMessageStatus = self.handleMessages
        self.getChats()

    def loadModules(self):
        cmds = {}
        cron = []

        for source in glob('modules/*.py'):
            name = source[8:-3]
            module = imp.load_source("!" + name, source)

            commands = module.getCommands()
            if commands:
                cmds.update(commands)

            jobs = module.getCron()
            if jobs:
                cron.extend(jobs)

        self.cmds = cmds
        self.cron = cron

    def getChats(self):
        chats = {}
        for chat in self.skype.Chats:
            chats[chat.FriendlyName] = chat
        self.chats = chats

    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        """
        if status == "RECEIVED" or status == "SENT":
            print("%s - %s - %s: %s" % (status, msg.Chat.FriendlyName, msg.FromHandle, msg.Body))
        if status == "RECEIVED" and msg.Body:
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

            if msg.Body[0] == "!":
                args = msg.Body.split(" ")
                try:
                    func = self.cmds[args[0]]
                    msg.Chat.SendMessage(func(
                            *args[1:],
                            msg=msg,
                            skype=self.skype,
                            bot=self
                        ))
                except Exception as e:
                    msg.Chat.SendMessage(str(e))

    def runCmd(self, cmd):
        args = cmd.split(" ")
        return self.cmds["!" + args[0]](*args[1:], bot=self, skype=self.skype)

    def sendMsg(self, chat, msg):
        self.chats[chat].SendMessage(msg)

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

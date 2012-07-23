# -*- coding: utf-8 -*-

from glob import glob
import imp
import time

import Skype4Py

class Sevabot:
    def __init__(self):
        self.cmds = {}
        self.cron = []
        self.loadModules()

        self.skype = Skype4Py.Skype(Transport='x11')
        self.skype.Attach()
        self.skype.OnMessageStatus = self.handleMessages

    def loadModules(self):
        cmds = {}
        cron = []

        for source in glob('modules/*.py'):
            name = source[8:3]
            module = imp.load_source("!"+name, source)
            
            commands = module.getCommands()
            if commands:
                cmds.update(commands)

            jobs = module.getCron()
            if jobs:
                cron.extend(jobs)

        self.cmds = cmds
        self.cron = cron

    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        """
        if status == "RECEIVED" or status == "SENT":
            print(status + " " + msg.FromHandle + ": " + msg.Body)
        if status == "RECEIVED":
            if msg.Body == "!loadModules":
                msg.Chat.SendMessage("Loading modules...")
                try:
                    self.loadModules()
                except Exception as e:
                    msg.Chat.SendMessage(str(e))
                    return

                return

            if msg.Body[0] == "!":
                args = msg.Body.split(" ")
                try:
                    msg.Chat.SendMessage(self.cmds[args[0]](msg=msg, *args[1:]))
                except Exception as e:
                    msg.Chat.SendMessage(str(e))

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
                    chat = [c for c in self.skype.Chats if c.FriendlyName == chat][0]
                    chats.append(chat)
                job['chats'] = chats

            job['timer'] -= interval

            if job['timer'] <= 0:
                try:
                    job['cmd'](chats=job['chats'])
                except Exception as e:
                    print("Error " + str(e))
                job['timer'] = job['interval']


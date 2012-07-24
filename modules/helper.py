# -*- coding: utf-8 -*-


def getchats(bot, *args, **kwargs):
    return "\n".join(bot.chats.keys())


def getCommands():
    return {"!chats": getchats}


def getCron():
    return []

# -*- coding: utf-8 -*-
"""

    Application entry point.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

from StringIO import StringIO
import imp
import sys
from hashlib import md5
import logging

from flask import Flask, request
import plac

logger = logging.getLogger("sevabot")

# http://docs.python.org/library/logging.html
LOG_FORMAT = "%(message)s"

server = Flask(__name__)

_sevabot = None


def get_bot():
    """
    We do lazy import here, because
    importing Skype4Py causes native DLL loading
    and may cause random segfaults, Skype pop-up dialogs or
    other unwanted side effects
    """
    global _sevabot
    if not _sevabot:
        from sevabot.bot import Sevabot
        _sevabot = Sevabot()

    return _sevabot


def get_settings():
    """
    Lazy init wrapper around settings.
    """
    import settings
    return settings


@plac.annotations( \
    settings=("Settings file", 'option', 's', None, None, "settings.py"),
    verbose=("Verbose debug output", 'option', 'v', None, None),
    )
def main(settings="settings.py", verbose=False):
    """
    Application entry point.
    """

    # Expose settings global module
    try:
        settings = imp.load_source("settings", settings)
    except:
        sys.exit("Could not load settings file: %s" % settings)

    # Config logging
    level = verbose if logging.DEBUG else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout, format=LOG_FORMAT)
    logger.info("Starting sevabot")

    from sevabot import modules
    modules.load_modules()

    sevabot = get_bot()

    logger.info("Skype API connection established")

    sevabot.start()
    server.run(settings.HTTP_HOST, settings.HTTP_PORT)

    # Should be never reached
    return 0


@server.route("/hello/")
def hello():
    """
    A simple HTTP interface test callback.
    """
    sevabot = get_bot()
    if sevabot:
        return "OK"
    else:
        return "UHOH"


@server.route("/chats/<string:shared_secret>/")
def chats(shared_secret):
    """
    Print out chats and their ids, so you can register external services against the chat ids.
    """
    sevabot = get_bot()
    chats = sevabot.getOpenChats()
    settings = get_settings()

    if shared_secret != settings.SHARED_SECRET:
        return ("Bad shared secret", 403, {"Content-type": "text/plain"})

    buffer = StringIO()
    for chat_id, chat in chats:
        print("%s: %s" % (chat_id, chat.FriendlyName), file=buffer)

    return (buffer.getvalue(), 200, {"Content-type": "text/plain; charset=utf-8"})


@server.route("/msg/", methods=['POST'])
def message():

    import settings

    sevabot = get_bot()

    try:
        if request.method == 'POST':
            if ('chat' in request.form and
               'msg' in request.form and
               'md5' in request.form):

                chat = request.form['chat']
                msg = request.form['msg']
                m = request.form['md5']

                mcheck = md5(chat + msg + settings.SHARED_SECRET).hexdigest()
                if mcheck == m:
                    return sevabot.sendMsg(chat, msg)
                else:
                    return "No can do\n"
    except Exception as e:
        return str(e)


@server.route("/github-post-commit/<int:chat_id>/<string:shared_secret>/", methods=['POST'])
def github_post_commit(chat_id, shared_secret):
    """
    Handle post-commit hook from Github.

    The URL is in format

    /github-post-commit/${chat-id}/${shared-secret}
    """

    settings = get_settings()
    sevabot = get_bot()


def entry_point():
    exit_code = plac.call(main)
    return exit_code

# -*- coding: utf-8 -*-
"""

    Application entry point.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import imp
import sys
import logging

from flask import Flask
from flask import render_template
from flask import request

import plac

from sevabot.frontend import api

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
        from sevabot.bot.bot import Sevabot

        _sevabot = Sevabot()

    return _sevabot


def get_settings():
    """
    Lazy init wrapper around settings.
    """
    import settings

    return settings


@plac.annotations(
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
    except Exception:
        sys.exit("Could not load settings file: %s" % settings)

    # Config logging
    level = verbose if logging.DEBUG else logging.INFO
    logging.basicConfig(level=level, stream=sys.stdout, format=LOG_FORMAT)
    logger.info("Starting sevabot")

    for skype_logger_name in ["Skype4Py.utils.EventHandlingBase", "Skype4Py.skype.Skype",
                              "Skype4Py.api.darwin.SkypeAPI"]:
        skype_logger = logging.getLogger(skype_logger_name)
        skype_logger.setLevel(logging.WARN)

    from sevabot.bot import modules

    modules.load_modules()

    sevabot = get_bot()

    logger.info("Skype API connection established")

    sevabot.start()

    api.configure(sevabot, settings, server)

    server.run(settings.HTTP_HOST, settings.HTTP_PORT, debug=False)

    # Should be never reached
    return 0


@server.route("/")
def root():
    """
    A simple HTTP interface test callback.
    """
    settings = get_settings()
    return render_template('index.html', host=settings.HTTP_HOST, port=settings.HTTP_PORT)


@server.route("/chats/", methods=["POST"])
def chats_post():
    """
    Print out chats and their ids, so you can register external services against the chat ids.
    """
    sevabot = get_bot()
    chats = sevabot.getOpenChats()
    settings = get_settings()

    shared_secret = request.form.get("secret")

    if shared_secret != settings.SHARED_SECRET:
        return "Bad shared secret", 403, {"Content-type": "text/plain"}

    return render_template('chats.html', chats=chats, shared_secret=shared_secret)


@server.route("/chat_message/<string:shared_secret>/<string:chat_id>/", methods=['GET'])
def chat_messages(shared_secret, chat_id):
    """
    A view to send a test message to a chat.
    """
    settings = get_settings()

    if shared_secret != settings.SHARED_SECRET:
        return "Bad shared secret", 403, {"Content-type": "text/plain"}

    return render_template('chat_message.html', chat_id=chat_id, shared_secret=shared_secret)


def entry_point():
    exit_code = plac.call(main)
    return exit_code


if __name__ == '__main__':
    entry_point()

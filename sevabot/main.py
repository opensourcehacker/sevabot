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
import json

from flask import Flask, request
import plac

logger = logging.getLogger("sevabot")

# http://docs.python.org/library/logging.html
LOG_FORMAT = "%(message)s"

server = Flask(__name__)

_sevabot = None

INTRO = """<!doctype html>
<h1><a href="https://github.com/sevanteri/sevabot">Sevabot</a></h1>

<p>
A generic purpose hack together Skype bot at your service.
</p>

<p>
For the chat list and other administrative HTTP interface functions
please read the README above.
</p>
"""


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

    for skype_logger_name in ["Skype4Py.utils.EventHandlingBase", "Skype4Py.skype.Skype", "Skype4Py.api.darwin.SkypeAPI"]:
        skype_logger = logging.getLogger(skype_logger_name)
        skype_logger.setLevel(logging.WARN)

    from sevabot import modules
    modules.load_modules()

    sevabot = get_bot()

    logger.info("Skype API connection established")

    sevabot.start()
    server.run(settings.HTTP_HOST, settings.HTTP_PORT)

    # Should be never reached
    return 0


@server.route("/")
def hello():
    """
    A simple HTTP interface test callback.
    """
    return INTRO


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

    print("Chat id                           Title", file=buffer)
    print("--------------------------------- -----------------------------", file=buffer)

    for chat_id, chat in chats:
        print("%s: %s" % (chat_id, chat.FriendlyName), file=buffer)

    return (buffer.getvalue(), 200, {"Content-type": "text/plain; charset=utf-8"})


@server.route("/msg/", methods=['POST'])
def message():
    """
    Receive a MD5 signed message into a chat.

    All parameters must be UTF-8, URL encoded when sending.

    MD5 is calculated for UTF-8 non-URL-encoded text.

    """
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

                chat_encoded = chat.encode("utf-8")
                msg_encoded = msg.encode("utf-8")

                mcheck = md5(chat_encoded + msg_encoded + settings.SHARED_SECRET).hexdigest()
                if mcheck == m:
                    sevabot.sendMsg(chat, msg)
                    return "OK"
                else:
                    logger.warning("MD5 check failed %s vs %s" % (mcheck, m))
                    logger.warning(request.form)
                    return "No can do\n"
            else:
                return ("Missing POST parameters", 500, {"Content-type": "text/plain"})

    except Exception as e:
        logger.error(e)
        logger.exception(e)
        return unicode(e)


@server.route("/github-post-commit/<string:chat_id>/<string:shared_secret>/", methods=['POST'])
def github_post_commit(chat_id, shared_secret):
    """
    Handle post-commit hook from Github.

    https://help.github.com/articles/post-receive-hooks/
    """

    settings = get_settings()
    sevabot = get_bot()

    if shared_secret != settings.SHARED_SECRET:
        return ("Bad shared secret", 403, {"Content-type": "text/plain"})

    #print(request.form.items())
    #print(request.form[":payload"])
    payload = json.loads(request.form["payload"])

    msg = "★ %s fresh commits 〜 %s\n" % (payload["repository"]["name"], payload["repository"]["url"])
    for c in payload["commits"]:
        msg += "★ %s: %s\n%s\n" % (c["author"]["name"], c["message"], c["url"])

    sevabot.sendMsg(chat_id, msg)

    return "OK"


@server.route("/zapier/<string:chat_id>/<string:shared_secret>/", methods=['POST'])
def zapier(chat_id, shared_secret):
    """
    Process incoming Zapier Webhook pushes.

    https://zapier.com/
    """

    settings = get_settings()
    sevabot = get_bot()

    try:

        if shared_secret != settings.SHARED_SECRET:
            return ("Bad shared secret", 403, {"Content-type": "text/plain"})

        msg = request.form["data"]

        sevabot.sendMsg(chat_id, msg)

        return "OK"

    except Exception as e:
        logger.error(request.form)
        logger.error(e)
        logger.exception(e)
        raise


def entry_point():
    exit_code = plac.call(main)
    return exit_code

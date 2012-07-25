# -*- coding: utf-8 -*-
"""

    Application entry point.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import imp
import time
from sevabot.bot import Sevabot

from hashlib import md5

from flask import Flask, request
import plac

server = Flask(__name__)
sevabot = Sevabot()


@plac.annotations( \
    settings=("Settings file", 'optional', 's', None, None, "settings.py"),
    )
def main(settings="settings.py"):
    """
    Application entry point.
    """

    # Expose settings global module
    settings = imp.load_source("settings", settings)

    print("Starting bot")
    server.run()

    #fuck cron stuff for now
    #interval = 1
    # while(True):
    #     time.sleep(interval)
    #     sevabot.runCron(interval)
    return 0


@server.route("/cmd/<string:cmd>")
def command(cmd):
    try:
        return sevabot.runCmd(cmd).replace("\n", "<br />")
    except Exception as e:
        return str(e)


@server.route("/msg/", methods=['POST'])
def message():
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
                    sevabot.sendMsg(chat, msg)
                else:
                    return "No can do %s\n" % (mcheck)
        return "Message sent"
    except Exception as e:
        return str(e)


def entry_point():
    exit_code = plac.call(main)
    return exit_code

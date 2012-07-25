# -*- coding: utf-8 -*-
"""

    Application entry point.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import time
from bot import Sevabot

from hashlib import md5

from flask import Flask, request

import plac


server = Flask(__name__)
sevabot = Sevabot()


@plac.annotations( \
    settings=("Settings file", 'positional', 's', None, None, "settings.py"),
    )
def main(settings="settings.py"):



    print("Starting bot")
    server.run()

    #fuck cron stuff for now
    #interval = 1
    # while(True):
    #     time.sleep(interval)
    #     sevabot.runCron(interval)


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


if __name__ == "__main__":
    exit_code = plac.call(main)
    sys.exit(exit_code)
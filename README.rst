===================
Sevabot for Skype
===================

.. contents:: local

Introduction
-------------

Sevabot is a generic purpose hack-it-together Skype bot

* Has extensible command system based on UNIX scripts

* Send chat message nofications from any system using HTTP requests

* Bult-in support for Github commit notifications and other popular services

It is based on `Skype4Py framework <https://github.com/stigkj/Skype4Py>`_

The bot is written in Python 2.7.x programming language, but can be integrated with any programming
languages over UNIX command piping and HTTP interface.

The underlying Skype4Py API is free - **you do not need to enlist and pay Skype development program fee**.

Use cases
-----------

* Get monitoring alerts to Skype from monitoring system like Zabbix

* Get alerts from continuous integration system build fails (Travis CI, Jenkins)

* Get notifications of new commits and issues in your software project (Git, SVN)

* Control production deployments from Skype chat with your fellow developers with in-house scripts

* Get a local weather

Benefits
-----------

Skype is the most popular work related chat program around the world.
Skype is easy: anyone can use Skype.

Skype group chat provides noise-free medium with a context.
People follow Skype more actively than email; the discussion in the group chat
around the notification messages feels natural.

For example our organization has an admin group chat where the team members
get notifications what other people are doing (commits, issues)
and when something goes wrong (monitoring). This provides pain free
follow up of the daily tasks.

A custom scripts can be thrown for the skype bot to execute:
these can be follow up actions like see that back-ups are running and up-to-date or
deployment actions like deploying the trunk on the production server
(As far as I know the latter use case is practiced Github internally).

Prerequisitements
------------------

OSX or Linux required. For running the bot on the server-side, a headless X must be installed.
Supporting Windows is possible, but currently lacks a sponsor for the feature.

First you need to `register a Skype account for your bot <http://skype.com>`_.

Ubuntu
========

Installing Skype and xvfb to your server. Under ``sudo -i``::

    useradd skype # We must run Skype under non-root user
    apt-get install xvfb
    apt-get install fluxbox x11vnc
    apt-get install dbus
    apt-get install libasound2 libqt4-dbus libqt4-network libqtcore4 libqtgui4 libxss1 libpython2.6 libqt4-xml libaudio2 libmng1 fontconfig liblcms1
    apt-get install lib32stdc++6 lib32asound2 ia32-libs libc6-i386 lib32gcc1
    wget http://www.skype.com/go/getskype-linux-beta-ubuntu-64 -O skype-linux-beta.deb
    # if there are other unresolved dependencies install missing packages using apt-get install and then install the skype deb package again
    dpkg -i skype-linux-beta.deb

Other packages and Python modules needed::

    apt-get install python-gobject-2 curl git

Setting up Skype and Sevabot

    #. Login to your server with: **ssh -L 5900:localhost:5900 skype@yourserver.com**
    #. Get Sevabot: **git clone git://github.com/sevanteri/sevabot.git**
    #. Start xvfb, fluxbox and Skype: **sevabot/scripts/start-server.sh start**
    #. Start vnc server: **sevabot/scripts/start-vcn.sh start**
    #. On your local computer start vnviewer: **vncviewer localhost**
    #. Login to Skype and save your username and password
    #. Got to Skype's settings and set the following
        - no chat history
        - only people on my list can write me
        - only people on my list can call me

Install ``sevabot`` using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/sevanteri/sevabot.git
    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    source venv/bin/activate
    python setup.py develop

OSX
====

These instructions are for desktop OSX.

`Install Skype <http://skype.com>`_.

Extra complications cause the fact that you need to create a 32-bit virtualenv
using Apple's fat binary ``python`` command.

Install ``sevabot`` using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/sevanteri/sevabot.git
    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    arch -i386 python virtualenv.py venv
    source venv/bin/activate
    arch -i386 python setup.py develop

Usage
------

Customize settings for you::

    # Create a copy of settings.py
    cp settings.py.example settings.py

Setup your Skype admin username and HTTP interface password by editing ``settings.py``.

Start Skype on the computer using the bot username.

Invite the bot to the Skype chat where you indent to run the bot.


Run on Ubuntu
==============

Activate virtualenv::

    . venv/bin/activate

Type::

  sevabot

Skype desktop app (in VNC) will now ask if Skype4Py should be allowed. **Click on Remember and Allow.**

Stop VNC server: **sevabot/scripts/start-vnc.sh stop**

Run on OSX
============

Type::

    arch -i386 sevabot

When you launch it for the first time you need to accept the confirmation dialog in the desktop
environment (over VNC on the server).

.. image :: https://github.com/downloads/sevanteri/sevabot/Screen%20Shot%202012-07-25%20at%201.13.57%20PM.png

or which ever display you're running your skype on your server.

.. note ::

    There might be a lot of logging and stdout output when the bot starts and scans all the chats of running Skype instance.

Eventually you see in the console::

    Running on http://127.0.0.1:5000/

Now you can send commands to the bot by typing them into the chat. All commands start with ``!``.
You can try ``!ping`` command see if the bot is alive. Type into chat::

    !ping

.. image :: https://github.com/downloads/sevanteri/sevabot/Screen%20Shot%202012-07-25%20at%202.33.48%20PM.png

You can also try stock ``!weather`` command::

    !weather helsinki

Integration
-------------

Creating custom commands
==============================

The bot can use any UNIX executables printing to stdout as commands

* Shell scripts

* Python scripts, Ruby scripts, etc.

All commands must be in one of *modules* folders of the bot. The bot comes with some built-in
commands like ``ping``, but you can add your own custom commands by

* Creating a new modules folder for your internal purposes - the name doesn't matter

* Put this folder to ``MODULES_PATHS`` in settings.py

* Create a a script in this folder. Example ``myscript.sh``::

    #!/bin/sh
    echo "Hello world from my sevabot command"

* Add UNIX execution bit on the script using ``chmod u+x myscript.sh``

* Restart bot

* Now you have command ``!myscript``

You can also use command ``!reload`` to reload all modules paths
if you have added new scripst in them. ``!reload`` will output
available commands.

Getting chat list
=======================

To send messages to the bot you need to know

* Skype chat id - we use MD5 encoded ids to conveniently pass them in URLs.

* Bot shared secret in ``settings.py``

To get list of the chat ids visit in the address::

    http://localhost:5000/chats/YOURSHAREDSECRET/

Sending messages to the chat from external service
====================================================

You can send a message to the bot over HTTP interface.

Messages are MD5 signed with a shared secret.

`Generic shell script example using curl can be found on Github <https://github.com/sevanteri/sevabot/blob/master/examples/send.sh>`_.

Github commit notifications
=============================

Sevabot has built-in support for Github post-receive hook a.k.a. commit notifications.

To add one

* You need to be the repository admin

* Go *Admin* > *Service hooks* on Github

* Add Webhooks URL with your bot info::

    http://yourserver.com:5000/github-post-commit/CHATID/SHAREDSECRET/

* Save

* Now you can use *Test hook* button to send a test message to the chat

* Following commits should come automatically to the chatß

Github issue notifications
================================

Use *Zapier* webhook as described below.

This applies for

* New Github issues

* New Github comments

Zapier Web hooks
=====================

`zapier.com <https://zapier.com/>`_ offers free mix-and-match
different event sources to different triggers. The event sources
includes popular services like Github, Dropbox, Salesforce, etc.

* You need to register your *zap* in zapier.com

* *Sevabot* offers support for Zapier web hook HTTP POST requests as JSON

* Create a zap in zapier.com. Register. Add Webhooks *URL* with your bot info::

    http://yourserver.com:5000/zapier/CHATID/SHAREDSECRET/

* The followning Zapier settings must be used: *Send as JSON: no*

* The Zapier data field is posted to the Skype chat as a message as is

Example of Zapier *Data* field for Github issues::

    ಠ_ಠ New issue 〜 {{title}} 〜 by {{user__login}} - {{html_url}}

Zabbix monitoring alerts
===========================

`Zabbix <http://www.zabbix.com/>`_ is a popular open source monitoring solution.

You can get Zabbix monitoring alerts like server down, disk near full, etc.
to Skype with *Sevabot*.


First you need to configure *Media* for your Zabbix user. The default user is called *Admin*.

Go to *Administrator* > *Media types*.

Add new media *Skype* with *Script name* **send.sh**.

Go to *Administrator* > *Users* > *Admin*. Open *Media* tab. Enable media *Skype* for this user.
In the *Send to* parameter put in your *chat id* (see instructions above).

On the server running the Zabbix server process
create a file ``/usr/local/share/zabbix/alertscripts/send.sh``::

    #!/bin/sh
    #
    # Example shell script for sending a message into sevabot
    #
    # Give command line parameters [chat id] and [message].
    # The message is md5 signed with a shared secret specified in settings.py
    # Then we use curl do to the request to sevabot HTTP interface.
    #
    #

    # Chat id comes as Send To parameter from Zabbix
    chat=$1

    # Message is the second parameter
    msg=$2

    # Our Skype bot shared secret
    secret="xxx"

    # The Skype bot HTTP msg interface
    msgaddress="http://yourserver.com:5000/msg/"

    md5=`echo -n "$chat$msg$secret" | md5sum`

    #md5sum prints a '-' to the end. Let's get rid of that.
    for m in $md5; do
        break
    done

    curl $msgaddress -d "chat=$chat&msg=$msg&md5=$m"

Subversion commit notifications
=================================

Short instructions::

    sudo -i
    wget -O sevabot.tar.gz --no-check-certificate https://github.com/opensourcehacker/sevabot/tarball/master

More info

* https://mikewest.org/2006/06/subversion-post-commit-hooks-101

Testing HTTP interface
========================

If you run the bot on non-internet facing computer (desktop)
you can tunnel HTTP interface to a public server::

    ssh -gNR 5000:yourserver.com:5000 yourserver.com

Troubleshooting
-----------------

Segfaults
===========

If you get segfault on OSX make sure you are using `32-bit Python <http://stackoverflow.com/questions/2088569/how-do-i-force-python-to-be-32-bit-on-snow-leopard-and-other-32-bit-64-bit-quest>`_.

`Debugging segmentation faults with Python <http://wiki.python.org/moin/DebuggingWithGdb>`_.

Related gdb dump::

    Program received signal EXC_BAD_ACCESS, Could not access memory.
    Reason: KERN_INVALID_ADDRESS at address: 0x0000000001243b68
    0x00007fff8c12d878 in CFRetain ()
    (gdb) bt
    #0  0x00007fff8c12d878 in CFRetain ()
    #1  0x00000001007e07ec in ffi_call_unix64 ()
    #2  0x00007fff5fbfbb50 in ?? ()
    (gdb) c
    Continuing.

    Program received signal EXC_BAD_ACCESS, Could not access memory.
    Reason: KERN_INVALID_ADDRESS at address: 0x0000000001243b68
    0x00007fff8c12d878 in CFRetain ()

Skype4Py distribution for OSX
===============================

Currently Skype4Py distribution is broken.

To fix this do::

    source venv/bin/activate
    git clone git://github.com/stigkj/Skype4Py.git
    cd Skype4Py
    arch -i386 python setup.py install


License
--------

BSD.

Authors
----------

`Pete Sevander <https://twitter.com/sevanteri>`_ - coding

`Mikko Ohtamaa <https://twitter.com/moo9000>`_ - concept, documentation and packing

Report issues on `Github <https://github.com/sevanteri/sevabot/issues>`_

Some documentation and scripts by `Marco Weber <http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/>`_

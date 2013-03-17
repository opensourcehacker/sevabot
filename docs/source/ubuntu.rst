============================================================
Installing and running on Ubuntu
============================================================

.. contents:: :local:

Introduction
===============

There instructions are for setting up a headless (no monitor attached) Sevabot running in Skype
on Ubuntu Server. The instructions have tested on Ubuntu Version **12.04.1** unless mentioned
otherwise.

.. note ::

    For desktop installation instructions see below.

Installing Skype and xvfb
=============================

Install Ubuntu dependencies needed to run headless Skype.

SSH into your server as a root or do ``sudo -i``.

Then install necessary software::

    apt-get update
    apt-get install -y xvfb fluxbox x11vnc dbus libasound2 libqt4-dbus libqt4-network libqtcore4 libqtgui4 libxss1 libpython2.7 libqt4-xml libaudio2 libmng1 fontconfig liblcms1 lib32stdc++6 lib32asound2 ia32-libs libc6-i386 lib32gcc1 nano
    wget http://www.skype.com/go/getskype-linux-beta-ubuntu-64 -O skype-linux-beta.deb
    # if there are other unresolved dependencies install missing packages using apt-get install and then install the skype deb package again
    dpkg -i skype-linux-beta.deb

More packages and Python modules needed to::

    apt-get install -y python-gobject-2
    apt-get install -y curl git

Setting up Skype and remote VNC
================================

Now we will create the UNIX user ``skype`` running Sevabot and Skype the client application.

.. note ::

    In this phase of installation you will need a VNC remote desktop viewer software
    on your local computer. On Linux you have XVNCViewer, on OSX you have Chicken of VNC
    and on Windows you have TinyVNC.

Under ``sudo -i``::

    # Create a random password
    openssl rand -base64 32  # Copy this output, write down and use in the input of the following command
    adduser skype # We must run Skype under non-root user

Exit from the current (root) terminal sessoin.

Login to your server::

    ssh skype@yourserver.example.com

Get Sevabot::

    git clone git://github.com/opensourcehacker/sevabot.git

.. note ::

    If you want to live dangerously you can use git dev branch where
    all the development happen. You can switch to this branch with "git checkout dev"
    command in the sevabot folder.

Start xvfb, fluxbox and Skype::

    # This will output some Xvfb warnings to the terminal for a while
    SERVICES="xvfb fluxbox skype" ~/sevabot/scripts/start-server.sh start

Start VNC server::

    # This will ask you for the password of VNC remote desktop session.
    # Give a password and let it write the password file.
    # Delete file ~/.x11vnc/password to reset the password
    ~/sevabot/scripts/start-vnc.sh start

On your **local computer** start the VNC viewing softare and connect the server::

    vncviewer yourserver.example.com  # Password as you give it above

You see the remote desktop. Login to Skype for the first time.
Make Skype to save your username and password. Create Skype
account in this point if you don't have one for sevabot.

.. image:: /images/skype-login.png
    :width: 500px

Now, in your **local** Skype, invite the bot as your friend. Then accept the friend request.

.. image:: /images/invite.png
    :width: 500px

.. note ::

    It is important to add one Skype buddy for your Sevabot instance in this point,
    so don't forget to do this step.

Nowm, in Sevabot go to Skype's settings and set the following

- No chat history

- Only people on my list can write me

- Only people on my list can call me

.. image:: /images/settings.png
    :width: 500px

Installing Sevabot
===================

When Skype is up and running on your server, you can attach Sevabot into it.

Sevabot is deployed as `Python virtualenv installation <http://opensourcehacker.com/2012/09/16/recommended-way-for-sudo-free-installation-of-python-software-with-virtualenv/>`_.

Login to your server as ``skype`` user over SSH::

    ssh skype@yourserver.example.com

Deploy ``sevabot``, as checked out from Github earlier, using `Python virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    . venv/bin/activate
    python setup.py develop

This will

- Pull all Python package dependencies from `pypi.python.org <http://pypi.python.org>`_ package service

- Create Sevabot launch scripts under ``~/sevabot/venv/bin/``

Set password and customize other Sevabot settings by creating and editing editing ``settings.py``::

    # Create a copy of settings.py
    cd ~/sevabot
    cp settings.py.example settings.py
    nano settings.py

In ``settings.py`` set

- ``SHARED_SECRET``: web interface password

- ``HTTP_HOST``: Public IP address you want Sevabot's web interface listen to (on Ubuntu you can figure this out using ``ipconfig command)

We need one more thing and that's accepting Skype dialog for Sevabot control in VNC session.
Make sure Xvfb, Fluxbox, Skype and VNC is running as instructed above. Do::

    # Start Sevabot and make initial connect attempt to Skype
    SERVICES=sevabot ~/sevabot/scripts/start-server.sh start

Authorize the connection and tick *Remember* in VNC session

.. image:: /images/authorize.png
    :width: 500px

Running sevabot
=================

To start the Sevabot do::

    # Following will restart Xvnx, Fluxbox, Skype and Sevabot
    ~/sevabot/scripts/start-server.sh restart

The last line you see should be something like::

    2013-03-17 18:45:16,270 - werkzeug - INFO -  * Running on http://123.123.123.123:5000/

.. note ::

    Make sure your IP address is right in above

From the log files see that Sevabot starts up::

    tail -f ~/sevabot/logs/sevabot.log

It should end up reading like this::

    Started Sevabot web server process

Test it
========

Start chatting with your Sevabot instance with your *local* Skype.

In Skype chat, type::

    !ping

Sevabot should respond to this message with Skype message::

    pong

.. note ::

    Sometimes Skype starts up slowly on the server and the initial messages are eaten by something.
    If you don't get instant reply, wait one minute and type !ping again.

Testing HTTP interface
========================

Sevabot server interface is listening to port 5000.
This interface offers

* Chat list (you need to know group chat id before you can send message into it)

* :doc:`Webhooks </webhooks>` for integrating external services

Just access the Sevabot server by going with your web browser to::

    http://yourserver.example.com:5000

.. image:: /images/admin.png
    :width: 500px

Troubleshooting
====================================

If you have problems see :doc:`Troubleshooting section for more information how to resolve them </troubleshooting>`.

Running sevabot as service
====================================

Sevabot and all related services can be controller with ``scripts/start-server.sh``
helper script. Services include

* Xvfb

* Fluxbox

* Skype

* Sevabot itself

Example::

    scripts/start-server.sh stop
    ...
    scripts/start-server.sh start
    ...
    scripts/start-server.sh status
    Xvfb is running
    fluxbox is running
    skype is running
    Sevabot running
    OVERALL STATUS: OK


To run sevabot from the server from reboot or do a full bot
restart there is an example script `reboot-seva.sh <https://github.com/opensourcehacker/sevabot/blob/master/scripts/reboot-seva.sh>`_ provided.
It also does optionally manual SSH key authorization so that
the bot can execute remote commands over SSH.

To make your Sevabot bullet-proof add `a cron job to check <https://github.com/opensourcehacker/sevabot/blob/master/scripts/check-service.sh>`_
that Sevabot is running correctly and reboot if necessary.

Setting avatar image
=======================

Sevabot has a cute logo which you want to set as Sevabot's Skype avatar image.

Here are short instructions.

Login as your sevabot user, tunnel VNC::

    ssh -L 5900:localhost:5900 skype@example.com

Start VNC::

    sevabot/scripts/start-vnc.sh start

On your local VNC client, connect to ``localhost:5900``.

Set the avatar image through Skype UI.

.. image:: /images/avatar.png
    :width: 500px

Installing on Ubuntu desktop
===============================

You don't need Xvfb, VNC or fluxbox.
These instructions were written for Ubuntu 12.04 64-bit.

.. note ::

    These instructions were written for running 32-bit Skype client application in 64-bit Ubuntu.
    Since writing the instructions the situation have changed and Skype has 64-bit application too.
    If you have insight of how to install these packages correctly please open an issue on Github
    and submit an updated recipe.

Install requirements and Skype::

    sudo -i

    apt-get install xvfb fluxbox x11vnc dbus libasound2 libqt4-dbus libqt4-network libqtcore4 libqtgui4 libxss1 libpython2.7 libqt4-xml libaudio2 libmng1 fontconfig liblcms1 lib32stdc++6 lib32asound2 ia32-libs libc6-i386 lib32gcc1

    apt-get install python-gobject-2 curl git

    wget http://www.skype.com/go/getskype-linux-beta-ubuntu-64 -O skype-linux-beta.deb
    # if there are other unresolved dependencies install missing packages using apt-get install and then install the skype deb package again
    dpkg -i skype-linux-beta.deb

    exit

Start Skype normally, register a new user or you can also use your own Skype account for testing..

Install Sevabot::

    git clone git://github.com/opensourcehacker/sevabot.git
    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    . venv/bin/activate
    python setup.py develop

Customize Sevabot settings::

    cp settings.py.example settings.py

Use your text editor to open ``settings.py`` and set your own password there.

Start sevabot::

    . venv/bin/activate
    sevabot

You should now see in your terminal::

    Skype API connection established
    getChats()
     * Running on http://localhost:5000/

Now enter with your browser to: `http://localhost:5000/ <http://localhost:5000/>`_.



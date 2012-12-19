============================================================
Installing and running on Ubuntu Server
============================================================

.. contents:: :local:

Introduction
===============

There instructions are for setting up a headless (no monitor attached) Sevabot running in Skype
on Ubuntu Server.

Installing Skype and xvfb
=============================

Install Ubuntu dependencies needed to run headless Skype.

We create UNIX user ``skype`` for running Sevabot.

Under ``sudo -i``::

    adduser skype # We must run Skype under non-root user
    apt-get install xvfb fluxbox x11vnc dbus libasound2 libqt4-dbus libqt4-network libqtcore4 libqtgui4 libxss1 libpython2.7 libqt4-xml libaudio2 libmng1 fontconfig liblcms1 lib32stdc++6 lib32asound2 ia32-libs libc6-i386 lib32gcc1
    wget http://www.skype.com/go/getskype-linux-beta-ubuntu-64 -O skype-linux-beta.deb
    # if there are other unresolved dependencies install missing packages using apt-get install and then install the skype deb package again
    dpkg -i skype-linux-beta.deb

Other packages and Python modules needed
=============================================

Under ``sudo -i``::

    apt-get install python-gobject-2 curl git

Setting up Skype and remote VNC
================================

Login to your server, opening tunnel to VNC port (see below)::

    ssh -L 5900:localhost:5900 skype@yourserver.com

Get Sevabot::

    git clone git://github.com/opensourcehacker/sevabot.git

Start xvfb, fluxbox and Skype::

    sevabot/scripts/start-server.sh start

Start vnc server::

    sevabot/scripts/start-vcn.sh start*

On your local computer start vnviewer (vncviewer is for Linux, for other OS
use any VNC capable remote desktop viewing software)
This will connect VNC viewrer to tunneled 5900 port on
the server so you can see the headless X desktop::

    vncviewer localhost

You see the remote desktop. Login to Skype for the first time.
Make Skype to save your username and password. Create Skype
account in this point if you don't have one for sevabot.

Got to Skype's settings and set the following

- no chat history
- only people on my list can write me
- only people on my list can call me

Installing sevabot
===================

Sevabot is deployed as `Python virtualenv installation <http://opensourcehacker.com/2012/09/16/recommended-way-for-sudo-free-installation-of-python-software-with-virtualenv/>`_.

Install ``sevabot`` using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    source venv/bin/activate
    python setup.py develop

This will

- Pull all Python package dependencies from *pypi.python.org*

- Create a scripts under ``venv/bin/`` to run Sevabot

Set password and other settings
======================================

Customize Sevabot settings::

    # Create a copy of settings.py
    cd ~/sevabot
    cp settings.py.example settings.py

Setup your Skype admin username and HTTP interface password by editing ``settings.py``.

Running sevabot
=================

Make sure headless Skype is running on the computer using the bot username (see above).

Create a group chat where you indent to use Sevabot.

Invite the Skype user to the Skype chat where you indent to run the bot.

Skype desktop app (in VNC) will now ask if Skype4Py should be allowed. **Click on Remember and Allow.**

Activate Python virtualenv proviving ``sevabot`` command::

    cd ~/sevabot
    . venv/bin/activate

To start the sevabot server in port 5000 type::

  sevabot

You should now see in your terminal::

    Skype API connection established
    getChats()
     * Running on http://localhost:5000/

Test it
========

In Skype chat, type::

    !ping

Sevabot should respond to this message with Skype message::

    pong

Reboot and detach proof sevabot
====================================

To run sevabot from the server from reboot

* Make sure X (xvfb) server is running

* Make sure Skype is running inside xvfb

* Make sure Sevabot server (port 5000)

* To make sure Sevabot server does not die from the terminal detach,
  use ``screen`` UNIX command


Assuming Sevabot is running under an UNIX user ``skype``.
We also assume that this bot needs
`SSH keys manually activated to execute certain scripts <http://opensourcehacker.com/2012/10/24/ssh-key-and-passwordless-login-basics-for-developers/>`_.

Start headless X, skype
::

     sudo -i -u skype
     sevabot/scripts/start-server.sh start
     # Warnings

Then start the bot script
::

    script /dev/null
    screen -t sevabot
    `eval ssh-agent` # Start SSH agent on ubuntu
    ssh-add # Active SSH keys manually with passpharse
    ../sevabot_venv/bin/sevabot # Run sevabot server

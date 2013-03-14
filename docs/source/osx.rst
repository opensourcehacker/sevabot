============================================================
Installing and running on OSX
============================================================

.. contents:: :local:

Introduction
===============

There instructions are for setting up a Sevabot to run on OSX desktop.

These instructions are mostly useful for Sevabot development and testing
and not for actual production deployments.

Installing Skype
=============================

Install Skype for OSX normally. Create your Skype user.

Installing sevabot
===================

Sevabot is deployed as `Python virtualenv installation <http://opensourcehacker.com/2012/09/16/recommended-way-for-sudo-free-installation-of-python-software-with-virtualenv/>`_.

Install ``sevabot`` using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/opensourcehacker/sevabot.git
    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    arch -i386 python virtualenv.py venv
    source venv/bin/activate
    arch -i386 python setup.py develop

This will

- Pull all Python package dependencies from *pypi.python.org*

- Create a scripts under ``venv/bin/`` to run Sevabot

.. note ::

    If you want to live dangerously you can use git dev branch where
    all the development happen.

Set password and other settings
======================================

Customize Sevabot settings::

    # Create a copy of settings.py
    cd ~/sevabot
    cp settings.py.example settings.py

Setup your Skype admin username and HTTP interface password by editing ``settings.py``.

Running sevabot
=================

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

Test it
========

In Skype chat, type::

    !ping

Sevabot should respond to this message with Skype message::

    pong

Testing HTTP interface
========================

Sevabot server interface is listening to port 5000.
This interface offers

* Chat list (you need to know group chat id before you can send message into it)

* :doc:`Webhooks </webhooks>` for integrating external services

Just access the Sevabot server by going with your web browser to::

    http://localhost:5000


.. image:: /images/admin.png
    :width: 500px

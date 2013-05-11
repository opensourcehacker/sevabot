============================================================
Installing and running on Windows
============================================================

.. contents:: :local:

Introduction
===============

There instructions are for setting up a Sevabot to run on Windows

These instructions are mostly useful for Sevabot development and testing
and not for actual production deployments.

Installing Skype
=============================

Install Skype for Windows normally. Don't install the Metro version on Windows 8. Create your Skype user.

Installing Python
==================

Install latest Python 2.X x86 version and add the installation folder to your PATH environment variable

Installing sevabot
===================

Sevabot is deployed as `Python virtualenv installation <http://opensourcehacker.com/2012/09/16/recommended-way-for-sudo-free-installation-of-python-software-with-virtualenv/>`_.    
Use Powershell x86 version to perform the following steps

Install ``sevabot`` using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/opensourcehacker/sevabot.git
    cd sevabot
    powershell -NoProfile -ExecutionPolicy unrestricted -Command "add-content -path virtualenv.py -value(new-object net.webclient).DownloadString('https://raw.github.com/pypa/virtualenv/master/virtualenv.py')"
    python virtualenv.py venv
    set-executionpolicy unrestricted
	. .\venv\Scripts\activate.ps1
    python setup.py develop

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
    cp settings.py.example settings.py

Setup your Skype admin username and HTTP interface password by editing ``settings.py``.

Running sevabot
=================

Type::

    venv\Scripts\sevabot.exe

When you launch it for the first time you need to accept the confirmation dialog in the desktop
environment

.. image :: /images/python_skype.png


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
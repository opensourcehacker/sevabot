=======
Sevabot
=======

.. contents:: local

Introduction
-------------

Generic purpose hack-it-together Skype bot

* Sends incoming messages to chat from any source over HTTP POST requests

* Will be able to run scripts and report

It is based on `Skype4Py framework <https://github.com/stigkj/Skype4Py>`_

Prerequisitements
------------------

OSX or Linux required. For running the bot on the server-side, a headless X must be installed.

Ubuntu
========

Packages and Python modules needed::

  apt-get install python-gobject-2 python-virtualenv

OSX
====

XXX

Installation
----------------

Install using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/sevanteri/sevabot.git
    cd sevabot
    virtualenv venv
    source venv/bin/activate
    python setup.py develop

Usage
------

Run with ::

  python2 main.py

or ::

  DISPLAY=:1 python2 main.py

or which ever display you're running your skype on your server.


Tested with python2.7.




=======
Sevabot
=======

.. contents:: local

Introduction
-------------

Generic purpose hack-it-together Skype bot

* Sends incoming messages to chat from any source over HTTP requests. This allows
  the bot to be connected to virtually any system.

* Will be able to run scripts and report

It is based on `Skype4Py framework <https://github.com/stigkj/Skype4Py>`_

Use cases
-----------

* Connect Skype to your server monitoring system like Zabbix

* Connect with continuous integration system

* Print out notifications of new commits and issues in your software project

* Run deployments directly from Skype

Prerequisitements
------------------

OSX or Linux required. For running the bot on the server-side, a headless X must be installed.

Ubuntu
========

Packages and Python modules needed::

    apt-get install python-gobject-2 python-virtualenv curl

OSX
====

Install with `Macports <http://www.macports.org/>`_.



Installation
----------------

Install using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

    git clone git://github.com/sevanteri/sevabot.git
    cd sevabot
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    source venv/bin/activate
    python setup.py develop


Setup your Skype admin username and HTTP interface password by editing ``settings.py``.

Usage
------

Run with ::

  python2 main.py

or ::

  DISPLAY=:1 python2 main.py

or which ever display you're running your skype on your server.


Tested with python2.7.

Authors
----------

`Pete Sevantari <https://twitter.com/sevanteri>`_ - coding

`Mikko Ohtamaa <https://twitter.com/moo9000>`_ - concept, documentation and packing

Report issues on `Github <https://github.com/sevanteri/sevabot/issues>`_


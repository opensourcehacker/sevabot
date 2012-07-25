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

Installation
---------------

OSX or Linux required.



Usage
------

Run with ::

  python2 main.py

or ::

  DISPLAY=:1 python2 main.py

or which ever display you're running your skype on your server.


Tested with python2.7.


Packages and python modules needed::

  apt-get install python-gobject-2
  easy_install-2.7 Flask
  easy_install-2.7 Skype4Py


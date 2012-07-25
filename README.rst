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

Installing Skype and xvfb to your server::

    useradd skype
    apt-get install xvfb
    apt-get install fluxbox x11vnc
    apt-get install dbus
    apt-get install libasound2 libqt4-dbus libqt4-network libqtcore4 libqtgui4 libxss1 libpython2.6 libqt4-xml libaudio2 libmng1 fontconfig liblcms1
    apt-get install lib32stdc++6 lib32asound2 ia32-libs libc6-i386 lib32gcc1
    wget http://www.skype.com/go/getskype-linux-beta-ubuntu-64 -O skype-linux-beta.deb
    # if there are other unresolved dependencies install missing packages using apt-get install and then install the skype deb package again
    dpkg -i skype-linux-beta.deb


Setting up Skype and Sevabot

    #. Login to your server with: **ssh -L 5900:localhost:5900 skype@your.zabbix.server**
    #. Get Sevabot: **git clone git://github.com/sevanteri/sevabot.git**
    #. Start xvfb, fluxbox and Skype: **sevabot/scripts/start-server.sh start**
    #. Start vnc server: **sevabot/scripts/start-vcn.sh start**
    #. On your local computer start vnviewer: **vncviewer localhost**
    #. Login to Skype and save your username and password
    #. Got to Skype's settings and set the following
        - no chat history
        - only people on my list can write me
        - only people on my list can call me
    #. Start Sevabot: **python2 sevabot/main.py**
        - Skype (in vnc) will now ask if Skype4Py should be allowed. **Click on Remember and Allow.**
    #. Stop vnc server: **sevabot/scripts/start-vnc.sh stop**


Other packages and Python modules needed::

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


Run bot with ::

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


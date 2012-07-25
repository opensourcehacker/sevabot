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
Supporting Windows is possible, but currently lacks a sponsor for the feature.

Python 2.7.x is supported. Python 3.x is not supported due to Skype4Py dependency.

First you need to `register a Skype account for your bot <http://skype.com>`_.

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

Other packages and Python modules needed::

    apt-get install python-gobject-2 curl

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

Install using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

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

Install using `virtualenv <http://pypi.python.org/pypi/virtualenv/>`_::

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

Activate virtualenv::

    . venv/bin/activate

Run on Ubuntu::

  sevabot

or ::

  DISPLAY=:1 python2 main.py

Run on OSX::

    arch -i386 sevabot

When you launch it for the first time you need to accept the confirmation dialog in the desktop
environment (over VNC on the server).

.. image :: https://github.com/downloads/sevanteri/sevabot/Screen%20Shot%202012-07-25%20at%201.13.57%20PM.png

or which ever display you're running your skype on your server.

There might be a lot of logging and stdout output when the bot scans all the chats of running Skype instance.

Sending messages to the chat from external service
-----------------------------------------------------

`Generic shell script can be found on Github <https://github.com/sevanteri/sevabot/blob/master/examples/send.sh>`_.

Troubleshooting
-----------------

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

License
--------

BSD.

Authors
----------

`Pete Sevander <https://twitter.com/sevanteri>`_ - coding

`Mikko Ohtamaa <https://twitter.com/moo9000>`_ - concept, documentation and packing

Report issues on `Github <https://github.com/sevanteri/sevabot/issues>`_

Some documentation and scripts by `Marco Weber <http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/>`_

======================
Troubleshooting
======================

.. contents:: :local:

Logging
===========

By default, Sevabot writes logging output to file ``logs/sevabot.log``.

You can watch this log in real time with UNIX command::

    tail -f logs/sevabot.log

To increase log level to max, edit ``settings.py`` and set::

    LOG_LEVEL = "DEBUG"

    DEBUG_HTTP = True

This will dump everything + HTTP request to the log.

Double messages
======================

Sevabot replies to all commands twice.

Still no idea what could be causing this. Restarting everything helps.

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

Skype messages not coming through to bot interface
==============================================================

Symptons

* Skype is running in Xvfb

* Sevabot logs in screen don't see incoming chat messages

Seems to happen if you reboot the bot in too fast cycle.
Maybe Skype login has something which makes it not working
if you log several times in a row.

Looks like it fixes itself if you just a wait a bit before sending
messages to the chat.

Crashing on a startup on Ubuntu server
==================================================

Segfault when starting up the bot::

      File "build/bdist.linux-i686/egg/Skype4Py/skype.py", line 250, in __init__
      File "build/bdist.linux-i686/egg/Skype4Py/api/posix.py", line 40, in SkypeAPI
      File "build/bdist.linux-i686/egg/Skype4Py/api/posix_x11.py", line 254, in __in                                    it__
    Skype4Py.errors.SkypeAPIError: Could not open XDisplay
    Segmentation fault (core dumped)

This usually means that your DISPLAY environment variable is wrong.

Try::

    export DISPLAY=:1

or::

    export DISPLAY=:0

depending on your configuration before running Sevabot.


Sevabot ignores commands and logs hang in sevabot - DEBUG - Attaching to Skype
====================================================================================================

This concerns only Ubuntu headless server deployments.

Your fluxbox might have hung. Kill it with fire::

    killall -SIGKILL fluxbox

Restart.


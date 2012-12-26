======================
Troubleshooting
======================

.. contents:: :local:

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


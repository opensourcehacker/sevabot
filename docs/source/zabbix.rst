============================================================
Zabbix alert messages from monitoring
============================================================

.. contents:: :local:

Introduction
===============

`Zabbix <http://www.zabbix.com/>`_ is a popular open source monitoring solution.

You can get Zabbix monitoring alerts like server down, disk near full, etc.
to Skype with *Sevabot*.

Setting up a webhook
======================

First you need to configure *Media* for your Zabbix user. The default user is called *Admin*.

Go to *Administrator* > *Media types*.

Add new media *Skype* with *Script name* **send.sh**.

Go to *Administrator* > *Users* > *Admin*. Open *Media* tab. Enable media *Skype* for this user.
In the *Send to* parameter put in your *chat id* (see instructions above).

On the server running the Zabbix server process
create a file ``/usr/local/share/zabbix/alertscripts/send.sh``::

    #!/bin/bash
    #
    # Example shell script for sending a message into sevabot
    #
    # Give command line parameters [chat id] and [message].
    # The message is md5 signed with a shared secret specified in settings.py
    # Then we use curl do to the request to sevabot HTTP interface.
    #
    #

    # Chat id comes as Send To parameter from Zabbix
    chat=$1

    # Message is the second parameter
    msg=$2

    # Our Skype bot shared secret
    secret="xxx"

    # The Skype bot HTTP msg interface
    msgaddress="http://yourserver.com:5000/msg/"

    md5=`echo -n "$chat$msg$secret" | md5sum`

    #md5sum prints a '-' to the end. Let's get rid of that.
    for m in $md5; do
        break
    done

    curl $msgaddress -d "chat=$chat&msg=$msg&md5=$m"


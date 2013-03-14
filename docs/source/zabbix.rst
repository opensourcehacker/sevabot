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

Doing a agent alive check
==============================

Below is a sample Sevabot script which will
do a Zabbix agent daemon check on all the servers.

See :doc:`commands </commands>` for how to configure SSH access
for Sevabot to perform this functionality.

* Make a fake alert on all monitor servers, listed in ~/.ssh/config of Sevabot UNIX user

* Zabbix alert script will report back this alert from all servers where Zabbix agent is correctly running

* You need to add a special trigger in Zabbix which checks a timestamp of ``/home/zabbix/zabbix_test``
  file, as touched by ``agents.sh`` run by Sevabot

Example monitoring item which keeps track of the file::

.. image:: /images/zabbix-item.png
    :width: 500px

.. note ::

    Depending on the UNIX user home the touch file may be
    /var/run/zabbix/zabbix_test or /home/zabbix/zabbix_test
    You might need to manualy switch Item state to Enabled after fixing this.

Example trigger:

.. image:: /images/zabbix-trigger.png
    :width: 500px

Then the script we give to Sevabot to poke the file over SSH to generate Information notification
in Zabbix and getting this notification back to our Zabbix monitoring Skype chat, confirming
the agent is alive and well.

``agents.sh``::

    #!/bin/bash
    #

    # Detect if we have a public key available
    ssh-add -L > /dev/null

    if [[ $? != "0" ]] ; then
        echo "Log-in as sevabot UNIX user and authorize SSH key"
        exit 1
    fi

    # Get list of hosts from SSH config file
    HOSTS=`grep "Host " ~/.ssh/config | awk '{print $2}'`

    # If some hosts don't have zabbix agents running, there's no need to use this script for them.
    # Add this line to ~/.ssh/config:
    # #NoAgents host1 host2
    NOAGENT=`grep "#NoAgents " ~/.ssh/config | cut -d' ' -f2- | tr ' ' '\n'`

    if [ -n "$NOAGENT" ]; then
        HOSTS=`echo -e "$HOSTS\n$NOAGENT" | sort | uniq -u`
    fi

    # Tell Sevabot what agents we are going to call
    echo "Agents: $HOSTS" | tr '\n' ' '
    echo


    errors=0

    # On each server touch a file to change its timestamp
    # Zabbix monitoring system will detect this and
    # report the alert back to Skype chat via a hook
    for h in $HOSTS; do
       ssh -o "PasswordAuthentication no" $h "touch -m zabbix_test"
       if [[ $? != "0" ]] ; then
        echo "Failed to SSH to $h as sevabot UNIX user"
            errors=1
       fi
    done

    if [[ $errors == "0" ]] ; then
        echo "Succesfully generated zabbix_test ping on all servers"
    fi

Example ``~/.ssh/config``::

    Host xxx
    User zabbix
    Hostname xxx.twinapex.fi

    Host yyy
    User zabbix
    Hostname yyy.twinapex.fi

Please note that you need to set up bot `SSH keys <http://opensourcehacker.com/2012/10/24/ssh-key-and-passwordless-login-basics-for-developers/>`_ for this.

Diagnosing

* If none of the agents is not replying your Zabbix host is probably messed up,
  reboot it: ``/etc/init.d/zabbix-server restart``

* If some of the agents are replying manually restart non-replying agents


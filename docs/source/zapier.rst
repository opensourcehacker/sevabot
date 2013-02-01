============================================================
Zapier webhook support
============================================================

.. contents:: :local:

Introduction
===============

`zapier.com <https://zapier.com/>`_ offers free mix-and-match
different event sources to different triggers. The event sources
includes popular services like Github, Dropbox, Salesforce, etc.

Zapier Web hooks (raw HTTP POSTs)
====================================

Zapier hook reads HTTP POST ``data`` variable payload to chat message as is.
It is useful for other integrations as well.

* You need to register your *zap* in zapier.com

* *Sevabot* offers support for Zapier web hook HTTP POST requests

* Create a zap in zapier.com. Register. Add Webhooks *URL* with your bot info::

    http://yourserver.com:5000/message_unsigned/

* Go to sevabot web interface and http://yourserver.com:5000/ get chat id from Skype

* The followning Zapier settings must be used: *Send as JSON: no*

* You need fill in HTTP POST fields *message* and *chat_id*

Example of Zapier *Data* field for Github issues::

    message|New issue 〜 {{title}} 〜 by {{user__login}} - {{html_url}}
    chat_id|YOURCHATIDHERE

.. image:: /images/zapier.png
    :width: 500px

Testing Zapier hook
---------------------

You can use ``curl`` to test the hook from your server, for firewall
issues and such::

    curl --data-binary "msg=Hello world" --data-binary "chat=YOURCHATID" http://localhost:5000/message_unsigned/

.. note::

    You need new enough curl version for --data-binary.

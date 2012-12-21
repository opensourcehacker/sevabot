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

* *Sevabot* offers support for Zapier web hook HTTP POST requests as JSON

* Create a zap in zapier.com. Register. Add Webhooks *URL* with your bot info::

    http://yourserver.com:5000/zapier/CHATID/SHAREDSECRET/

* The followning Zapier settings must be used: *Send as JSON: no*

* The Zapier data field is posted to the Skype chat as a message as is

Example of Zapier *Data* field for Github issues::

    New issue 〜 {{title}} 〜 by {{user__login}} - {{html_url}}

Testing Zapier hook
---------------------

You can use ``curl`` to test the hook from your server, for firewall
issues and such::

    curl --data-binary "data=Your message" "http://server:5000/zapier/CHATID/YOURSECRET/"
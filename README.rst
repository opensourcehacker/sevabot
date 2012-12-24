.. contents::

Introduction
-------------

.. image:: https://github.com/opensourcehacker/sevabot/raw/master/docs/source/images/sevabot-64.png
    :align: left

Sevabot is a generic purpose hack-it-together Skype bot

* Has extensible command system based on UNIX scripts

* Send chat message nofications from any system using HTTP requests

* Bult-in support for Github commit notifications and other popular services

It is based on `Skype4Py framework <https://github.com/stigkj/Skype4Py>`_

The bot is written in Python 2.7.x programming language, but can be integrated with any programming
languages over UNIX command piping and HTTP interface.

The underlying Skype4Py API is free - **you do not need to enlist and pay Skype development program fee**.

Use cases
-----------

Developer oriented use cases include

* Get monitoring alerts to Skype from monitoring system like Zabbix

* Get alerts from continuous integration system build fails (Travis CI, Jenkins)

* Get notifications of new commits and issues in your software project (Git, SVN)

* Control production deployments from Skype chat with your fellow developers with in-house scripts

Benefits
-----------

Skype is the most popular work related chat program around the world.
Skype is easy: anyone can use Skype.

Skype group chat provides noise-free medium with a context.
People follow Skype more actively than email; the discussion in the group chat
around the notification messages feels natural.

For example our organization has an admin group chat where the team members
get notifications what other people are doing (commits, issues)
and when something goes wrong (monitoring). This provides pain free
follow up of the daily tasks.

A custom scripts can be thrown for the skype bot to execute:
these can be follow up actions like see that back-ups are running and up-to-date or
deployment actions like deploying the trunk on the production server
(As far as I know the latter use case is practiced Github internally).

Supported operating systems
-----------------------------

* `Ubuntu Server (headless server installation) <https://sevabot-skype-bot.readthedocs.org/en/latest/ubuntu.html>`_

* `OSX desktop <https://sevabot-skype-bot.readthedocs.org/en/latest/osx.html>`_

* `Vagrant virtual machien deployments <https://sevabot-skype-bot.readthedocs.org/en/latest/vagrant.html>`_

Windows installation works in theory, but currently no core developer run Windows.

Example integrations
-----------------------

Sevabot can

* run any UNIX scripts and executable on the server and output the result to Skype chat

* delegate messages from external services to Skype chat over HTTP interface

Here are some examples

* `Bash shell script as a Skype group chat command <https://sevabot-skype-bot.readthedocs.org/en/latest/commands.html#creating-custom-commands>`_

* `Bash shell script sending Skype chat messages from an external service <https://sevabot-skype-bot.readthedocs.org/en/latest/bash.html>`_

* `Subversion commit notifications <https://sevabot-skype-bot.readthedocs.org/en/latest/subversion.html>`_

* `Github issue and commit notifications <https://sevabot-skype-bot.readthedocs.org/en/latest/github.html>`_

* `Zabbix monitoring alerts <https://sevabot-skype-bot.readthedocs.org/en/latest/zabbix.html>`_

* `Jenkins continuous integration status <https://sevabot-skype-bot.readthedocs.org/en/latest/jenkins.html>`_

Documentation
----------------

`Browser Sevabot documentation on readthedocs.org <https://sevabot-skype-bot.readthedocs.org/en/latest/>`_.

Community, support and development
------------------------------------

`See community information <https://sevabot-skype-bot.readthedocs.org/en/latest/development.html>`_

License
--------

BSD.

Authors
----------

`Mikko Ohtamaa <https://twitter.com/moo9000>`_ - concept, documentation and packing

`Pete Sevander <https://twitter.com/sevanteri>`_ - initial implementation

`Grigory Chernyshev <https://github.com/grundic>`_ - Valgrind, other

`Brian Johnson <https://github.com/b2jrock>`_ - Jenkins

`Felix Mueller <https://github.com/lixef>`_ - scripts

Some documentation and scripts by `Marco Weber <http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/>`_

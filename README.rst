===================
Sevabot for Skype
===================

.. contents:: local

Introduction
-------------

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

* Ubuntu Server (headless installation)

* OSX

* Vagrant virtual machien deployments

Documentation
----------------

`Browser Sevabot documentation on readthedocs.org <>`_.

Issues and source
------------------

Report issues on `Github <https://github.com/opensourcehacker/sevabot/issues>`_

License
--------

BSD.

Authors
----------

`Mikko Ohtamaa <https://twitter.com/moo9000>`_ - concept, documentation and packing

`Pete Sevander <https://twitter.com/sevanteri>`_ - initial implementation

`Grigory Chernyshev <https://github.com/grundic>`_ - Valgrind, other

`Felix Mueller <https://github.com/lixef>`_ - scripts


`

Some documentation and scripts by `Marco Weber <http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/>`_

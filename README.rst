.. contents::



Note: **Microsoft is in proceed to kill third party API for Skype.**
    
`Change.org petition to stop Microsoft <http://www.change.org/en-CA/petitions/skype-microsoft-provide-continued-support-for-third-party-skype-utilities-that-have-become-mission-critical-to-skype-s-users>`_
    
http://www.theregister.co.uk/2013/11/07/skype_desktop_u_turn/

http://voiceontheweb.biz/skype-world/skype-markets-skype-world/skype-for-business/skype-abandoning-developers-inviting-user-backlash/

Introduction
-------------

.. image:: https://github.com/opensourcehacker/sevabot/raw/master/docs/source/images/sevabot-64.png
    :align: left

Sevabot is a generic purpose hack-it-together Skype bot

* Has extensible command system based on UNIX scripts

* Send chat messages from anywhere using HTTP requests and webhooks

* Bult-in support for Github commit notifications and other popular services

It is based on `Skype4Py framework <https://github.com/awahlig/skype4py>`_

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

Installation and supported operating systems
----------------------------------------------------------

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

Testimonies
----------------

Nate:

    We've been looking for a Campfire replacement for a while and we all already use Skype.
    It was pretty easy to get going.

Documentation
----------------

`Browser Sevabot documentation on readthedocs.org <https://sevabot-skype-bot.readthedocs.org/en/latest/>`_.

Community, support and development
------------------------------------

`See community information <https://sevabot-skype-bot.readthedocs.org/en/latest/development.html>`_

Elsewhere

* `Building Skype chat bots in Python <http://opensourcehacker.com/2013/03/28/building-chat-applications-and-robots-for-skype/>`_

Commercial support
------------------------------------

Please feel free to sask commercial support from the `authors of the software <http://redinnovation.com/>`_

License
--------

BSD.

Authors
----------

Mikko Ohtamaa (`blog <https://opensourcehacker.com>`_, `Facebook <https://www.facebook.com/?q=#/pages/Open-Source-Hacker/181710458567630>`_, `Twitter <https://twitter.com/moo9000>`_, `Google+ <https://plus.google.com/u/0/103323677227728078543/>`_) - concept, documentation and maintainer

`Pete Sevander <https://twitter.com/sevanteri>`_ - initial implementation

`Grigory Chernyshev <https://github.com/grundic>`_ - Valgrind, other

`Brian Johnson <https://github.com/b2jrock>`_ - Jenkins

`Antti Haapala <https://github.com/ztane>`_ - Python best pratice fixes

`Naoto Yokoyama <https://github.com/builtinnya>`_ - message handler classfication, clean up

`Felix Mueller <https://github.com/lixef>`_ - scripts

Some documentation and scripts by `Marco Weber <http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/>`_

Trademark notice
-----------------

The Skype name, associated trade marks and logos and the "S" logo are trade marks of Skype or related entities.
Sevabot is an open source project and not associate of Microsoft Corporation or Skype.

Changes
---------

`See dev branch changes <https://github.com/opensourcehacker/sevabot/blob/dev/CHANGES.rst>`_


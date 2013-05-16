============================================================
Github notifications to Skype
============================================================

.. contents:: :local:

Introduction
===============

Github notifications are provided through natively through Github and
via :doc:`Zapier middleman service </zapier>`.

Commit notifications
=============================

Sevabot has built-in support for Github post-receive commit notifications.

To add one

* You need to be the repository admin

* Go *Admin* > *Service hooks* on Github

* Add Webhooks URL with your bot info::

    http://yourserver.com:5000/github-post-commit/CHATID/SHAREDSECRET/

* Save

* Now you can use *Test hook* button to send a test message to the chat

* Following commits should come automatically to the chatß

Pull request notifications
=============================

Sevabot has built-in support for Github post-receive pull request notifications.

To add one

* You need to be the repository admin

* Go *Admin* > *Service hooks* on Github

* Add Webhooks URL with your bot info::

    http://yourserver.com:5000/github-pull-request/CHATID/SHAREDSECRET/

* Save

* Using curl and GitHub API edit the above webhook by using the PATCH verb and JSON string of {"active":true,"add_events":["pull_request"]}

    See http://developer.github.com/v3/repos/hooks/ for more details on webhook editing through the GitHub API

* Whenever new pull requests are opened or closed a notification should come automatically to the chatß

Issue notifications
================================

Use *Zapier* webhook as described below.

This applies for

* New Github issues

* New Github comments

:doc:`See generic Zapier instructions how to set-up the hook </zapier>`.
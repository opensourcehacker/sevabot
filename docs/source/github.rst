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

Sevabot has built-in support for Github post-receive hook a.k.a. commit notifications.

To add one

* You need to be the repository admin

* Go *Admin* > *Service hooks* on Github

* Add Webhooks URL with your bot info::

    http://yourserver.com:5000/github-post-commit/CHATID/SHAREDSECRET/

* Save

* Now you can use *Test hook* button to send a test message to the chat

* Following commits should come automatically to the chatß

Issue notifications
================================

Use *Zapier* webhook as described below.

This applies for

* New Github issues

* New Github comments

:doc:`See generic Zapier instructions how to set-up the hook </zapier>`.
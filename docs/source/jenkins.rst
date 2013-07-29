============================================================
Jenkins continuous integration notifications
============================================================

.. contents:: :local:

Introduction
===============

`Jenkins <http://jenkins-ci.org/>`_ is a popular open source continuous integration server.

Jenkins supports webhook notifications by using the Notification plugin:
https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin

The jenkins notifier will emit build status through skype.

Setting up a webhook
======================

Install the plugin as directed in the above wiki link.

In Jenkins, for each build you want to send notifications for, under the 'Job Notifications' section, click 'Add Endpoint'.

Select 'JSON' and 'HTTP' in the ''Format' and 'Protocol' drop-down menus, respectively.

Enter your sevabot jenkins-notification endpoint, for example:
http://sevabot.example.com:5000/jenkins-notifier/{your-channel-id}/{your-shared-secret}/

Trailing slash is important.

When a build completes, you should see the bot emit a message with the build status.


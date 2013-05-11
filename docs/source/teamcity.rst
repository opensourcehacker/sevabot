============================================================
TeamCity webhook support
============================================================

.. contents:: :local:

Introduction
===============

`TeamCity <http://www.jetbrains.com/teamcity/>` is a popular continuous integration server from JetBrains.

TeamCity supports webhook notifications by using the tcWebHooks plugin:
http://tcplugins.sourceforge.net/info/tcWebHooks

Setting up a webhook
======================

Install the plugin as directed in the link below
http://sourceforge.net/apps/trac/tcplugins/wiki/TcWebHooks

Then in TeamCity, for each project you want to send notifications for, under the 'Web Hooks' section, click 'Edit Project Web Hooks' then click on '+ Click to create new WebHook for this project'

Enter your sevabot unsigned message notification endpoint, for example:

http://yourserver.com:5000/message_unsigned/

Trailing slash is important.

The followning Web Hook Payload Format setting must be used: *Name Value Pairs*

Go to sevabot web interface and http://yourserver.com:5000/ get chat id from Skype

On TeamCity server edit the ${HOME}/.BuildServer/config/{ProjectName}/plugin-settings.xml file and add the following after the closing tag of your webhook state tag ``i.e. </states>``.

``<parameters>``
``<param name="chat_id" value="{SkypeChatID}" />`` 
``</parameters>``

When a TeamCity build under this project completes, you should see the bot emit a message with the build status.

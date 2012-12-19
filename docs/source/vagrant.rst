============================================================
Installing and running using Vagrant
============================================================

.. contents:: :local:

Introduction
===============

`Vagrant <http://vagrantup.com/>`_ is a tool to setup and deploy local virtual machines
easily. Sevabot has a script for creating Vagrant deployments.

Vagrant it
====================================

Here is deployment instructions for
deployment and automatic virtual machine configuration::

    git clone https://github.com/opensourcehacker/sevabot.git
    cd sevabot
    vagrant box add precise64 http://files.vagrantup.com/precise64.box
    vagrant up

Now you should have a virtual machine running having a runnign Sevabot in it.

TODO (these instructions might need someone to have a look of them as I don't use Vagrant myself -MIkko)
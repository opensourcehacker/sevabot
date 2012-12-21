============================================================
Chat commands
============================================================

.. contents:: :local:

Introduction
===============

Sevabot supports commands you can type into group chat.
All commands begin with !.

You can create your own commands easily as Sevabot
happily executes any UNIX executable script.

Out of the box commands
==============================

Here are commands sevabot honours out of the box.

You can type them into the sevabot group chat.

* !reload: Reload current command scripts and print the list of available commands

* !ping: Check the bot is alive

* !weather: Get weather by a city from `openweathermap.org <http://openweathermap.org/>`_. Example: ``!weather Toholampi``

* !timeout: Test timeouting commands

* !soundcloud: Get your soundclound playlist (edit soundcloud.rb to make it work)

Creating custom commands
==============================

The bot can use any UNIX executables printing to stdout as commands

* Shell scripts

* Python scripts, Ruby scripts, etc.

All commands must be in one of *modules* folders of the bot. The bot comes with some built-in
commands like ``ping``, but you can add your own custom commands by

* Creating a new modules folder for your internal purposes - the name doesn't matter

* Put this folder to ``MODULES_PATHS`` in settings.py

* Create a a script in this folder. Example ``myscript.sh``::

    #!/bin/sh
    echo "Hello world from my sevabot command"

* Add UNIX execution bit on the script using ``chmod u+x myscript.sh``

* In Sevabot chat, type command  ``!reload`` to re-read ``scripts`` folder

* Now you should see command ``!myscript`` in the command list


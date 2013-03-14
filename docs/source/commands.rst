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

* !sad: No woman, no cry

* !weather: Get weather by a city from `openweathermap.org <http://openweathermap.org/>`_. Example: ``!weather Toholampi``

* !timeout: Test timeouting commands

* !soundcloud: Get your soundclound playlist (edit soundcloud.rb to make it work)

* !dice: Throw a dice

* !tasks: A simple ah-hoc group task manager for virtual team sprints

* !call: Conference call manager. Type ``!call help`` for more info.

Creating custom commands
==============================

The bot can use any UNIX executables printing to stdout as commands

* Shell scripts

* Python scripts, Ruby scripts, etc.

All commands must be in one of *modules* folders of the bot. The bot comes with some built-in
commands like ``ping``, but you can add your own custom commands by

* There is a ``custom/`` folder where you can place your own modules

* Enable ``custom`` folder in settings.py

* Create a a script in ``custom`` folder. Example ``myscript.sh``::

    #!/bin/sh
    echo "Hello world from my sevabot command"

* Add UNIX execution bit on the script using ``chmod u+x myscript.sh``

* In Sevabot chat, type command  ``!reload`` to relaod all scripts

* Now you should see command ``!myscript`` in the command list

* The following environment variables are exposed to scripts ``SKYPE_USERNAME``, ``SKYPE_FULLNAME``
  from the person who executed the command

Stateful modules
============================================================

You can have Python modules which maintain their state and have
full access to Skype4Py instance. These modules can e.g.

* Perform timed background tasks with Skype

* Parse full Skype chat text, not just !commands

* Reach to calls, initiate calls

* Send SMS, etc.

Further info

- `Stateful module interface is described here <https://github.com/opensourcehacker/sevabot/blob/dev/sevabot/bot/stateful.py>`_

- `Example task manager module is here <https://github.com/opensourcehacker/sevabot/blob/dev/modules/tasks.py>`_

- `Example conference call module is here <https://github.com/opensourcehacker/sevabot/blob/dev/modules/call.py>`_


Running commands on remote servers
============================================================

The best way to execute commands on remote servers
on UNIX is over SSH.
Please read first the
`basics how to setup SSH keys for the bot <http://opensourcehacker.com/2012/10/24/ssh-key-and-passwordless-login-basics-for-developers/>´_.

Below is an example ``backup.sh`` which checks

* disk space usage

* the timestamp

of backup folders on a backup server over SSH.

``backup.sh``::

    #!/bin/sh

    ssh root@example.com '
    LOCATION="/srv/backup/backup/duply"
    for l in $LOCATION/*; do
        S=`du -sh $l`
        TIME=`stat -c %y $l | cut -d " " -f1`
        BPATH=`echo $S | cut -f2`
        SIZE=`echo $S | cut -f1`

        echo -e "$SIZE\t$TIME\t$BPATH"
    done
    '#


You you need to install SSH keys on ``skype`` user to contact these servers::

    ssh -a skype@sevabotserver.example.com

    # Create key for the bot if one doesn't exist in .ssh/id_rsa
    # Note: For safety reasons set passpharse. See reboot-seva script
    # how passphrase enabled key is handled
    ssh-keygen

    # Copy the key to the remote server where you indent to run SSH commands
    ssh-copy-id targetuser@targetserver.com






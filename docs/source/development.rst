============================================================
Community and development
============================================================

.. contents:: :local:

Introduction
===============

How to participate to the spectacular future of Sevabot.
You can make the life of Sevabot better - and yours too!

IRC
====

For chatting

/join #opensourcehacker @ irc.freenode.net

Note: due to low activity of the channel prepare to idle there
for 24 hours to wait for the answer.

Support tickets and issues
=============================

`Use Github issue tracker <https://github.com/opensourcehacker/sevabot/issues>`_

Installing development version
==========================================================

All development happens in ``dev`` branch.

How to install and run the development version (trunk) of Sevabot::

    git clone git://github.com/opensourcehacker/sevabot.git
    cd sevabot
    git checkout dev
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv # prefix with arch -i386  on OSX
    source venv/bin/activate
    python setup.py develop # prefix with arch -i386  on OSX

Debugging
===========

You might want to turn on ``DEBUG_HTTP`` setting to dump out incoming HTTP requests
if you are testing / developing your own hooks.

Contributions
==========================================================

All contributions must come with accompaning documentation updates.

All Python files must follow PEP-8 coding conventionas and be `flake8 valid <http://pypi.python.org/pypi/flake8/>`_.

Submit pull request at Github.

For any changes update `CHANGES.rst <https://github.com/opensourcehacker/sevabot/blob/master/CHANGES.rst>`_.


Releases
=========

`Use zest.releaser <http://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/>`_

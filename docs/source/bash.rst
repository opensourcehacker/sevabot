============================================================
Sending Skype messages from shell scripts
============================================================

.. contents:: :local:

Introduction
===============

These examples use an out-dated web API. Until the documentation is properly updated, you can post a message with the following commandline:

    curl --data-urlencode chat_id="..." --data-urlencode message="..." --data-urlencode shared_secret="..." http://localhost:5000/message/

See examples (bash specifc)

* `send.sh <https://github.com/opensourcehacker/sevabot/blob/master/examples/send.sh>`_

* `ci-loop.bash <https://github.com/opensourcehacker/sevabot/blob/master/examples/ci-loop.bash>`_

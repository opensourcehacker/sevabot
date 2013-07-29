Changelog for Sevabot
-------------------------

1.2.5 (2013-07-29)
------------------

- Updated Jenkins notification webhook to work with v1.5 of the Jenkins notification plugin [justnom]


1.2.4 (2013-03-17)
------------------

- Make sure the bot doesn't reply to messages twice if a funny Skype client/device is attached to a group chat [miohtama]

1.2.3 (2013-03-17)
------------------

- Reworked start up scripts and installation manual [miohtama]

1.2.2 (2013-03-14)
------------------

- Fixed MD5 checksum check in triggers [miohtama]

- Allow write log level name in lowercase in settings.py [miohtama]


1.2 (2013-03-14)
----------------

- Addeds !tasks, !call and !dice example module [miohtama, builtinnya]

- Added stateful, class-based, command handlers [miohtama, builtinnya]

- Added more options to increase log level and DEBUG_HTTP setting [miohtama]

- Reworking unsigned HTTP POST message hooks */zapier* and */message_unsigned* [miohtama]

- Fixed Skype message unicode handling on OSX - caused Sevabot to ignore commands [miohtama]

- More robust error messages with webhooks and commands [miohtama]

- Workaround hanging fluxbox problems in the startup script example [miohtama]

1.1 (2013-02-01)
----------------

- Use shlex for command line parsing [ztane]

- Interleave stdout and stderr in output [ztane]

- Moved chunk of troubleshooting stuff to Skype4Py itself [miohtama]

- Made some backwards compatiblity adjustment in webhook parameters,
  so that all existing examples and demo scripts work [miohtama]

- Made it possible to run Sevabot as a background service using --daemon switch [miohtama]

- Updated launch scripts to be more robust and simple [miohtama]

- Security fix to prevent arbitrary commands from being executed [b2jrock]

1.0 (2012-12-24)
----------------

- Initial PyPi release [miohtama]


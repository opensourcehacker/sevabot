Changelog for Sevabot
-------------------------

1.2 (unreleased)
----------------

- Added Dice example module [builtinnya]

- Addeds Tasks example module [miohtama]

- Added class-based command handlers [builtinnya]

- Added log levels [builtinnya]

- Added DEBUG_HTTP setting [miohtama]

- Reworking unsigned HTTP POST message hooks */zapier* and */message_unsigned* [miohtama]

- Pass "no chat found" error to the HTTP client [miohtama]

- Fixed Skype message unicode handling on OSX - caused Sevabot to ignore commands [miohtama]

- Sevabot replies when it receives an unknown command [miohtama]

- Workaround hanging fluxbox problems [miohtama]

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


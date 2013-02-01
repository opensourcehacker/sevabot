#!/bin/sh
#
# Send an unsigned message using only HTTP POST *data* parameter and pass chat id in URL
#
# On OSX you need:
#
#   sudo port install md5sha1sum
#

chat=$1
msg=$2
secret="secret"
msgaddress="http://localhost:5000/zapier/$chat/$secret/"

curl $msgaddress --data-urlencode msg="$msg"
#!/bin/sh


chat=$1
msg=$2
secret="TheCakeIsALie"
msgaddress="http://localhost:5000/msg/"

md5=`echo -n "$chat$msg$secret" | md5sum`

#md5sum prints a '-' to the end. Let's get rid of that.
for m in $md5; do
    break
done

curl $msgaddress -d "chat=$chat&msg=$msg&md5=$m"

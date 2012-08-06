#!/bin/sh
#
# Subversion post commit hook example. Please change YOUR parts.
#
# - Drop this file as post-commit in /srv/svnrepts/YOURREPO/hooks 
# - chmod u+x
# - Change owner to www-data:www-data if you are running Subversion under Apache: chown www-data:www-data post-commit
#
# http://www.jasongrimes.org/2011/07/automatically-announce-subversion-commits-on-yammer-with-svn2yammer/
#
# To test this example run on the server:
#
# /usr/bin/svnlook youngest /srv/svnreps/red # get revision
# /srv/svnreps/red/hooks/post-commit /srv/svnreps/red 11301 # Test msg push
#

repo="$1"

rev="$2"

svnlook="/usr/bin/svnlook"

# Get last commit author
author=`$svnlook author $repo`

# Get last commit message
commit_message=`$svnlook log $repo`

# List of changed files
changed=`$svnlook changed $repo`

# Chat id
chat="YOUR-CHAT-ID-HERE"

# Shared secret
secret="YOUR-SHARED-SECRET-HERE"

msg="★ $author - $commit_message
$changed"

msgaddress="http://YOURSERVER.COM:5000/msg/"

md5=`echo -n "$chat$msg$secret" | md5sum`

#md5sum prints a '-' to the end. Let's get rid of that.
for m in $md5; do
    break
done

curl $msgaddress --data-urlencode chat="$chat" --data-urlencode msg="$msg" --data-urlencode md5="$m"

exit 0

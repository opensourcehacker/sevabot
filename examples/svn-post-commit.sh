#!/bin/sh
#
# Subversion post commit hook example.
#
# Drop this file as post-commit in /srv/svnrepts/YOURREPO/hooks and chmod a+x
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
chat="9d2588e144cc0afb7678222facad7490"

# Shared secret
secret="390y672349"

msg="★ $author - $commit message\n$changed"

msgaddress="http://guinness.twinapex.fi:5000/msg/"

md5=`echo -n "$chat$msg$secret" | md5sum`

#md5sum prints a '-' to the end. Let's get rid of that.
for m in $md5; do
    break
done

curl $msgaddress --data-urlencode "chat=$chat&msg=$msg&md5=$m"

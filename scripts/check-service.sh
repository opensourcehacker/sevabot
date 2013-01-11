#!/bin/bash
#
# Check that sevabot service is runnign correctly and
# reboot it if necessary. Intended to be run as a cron job.
#
# Add in /etc/cron.hourly/check-seva
#
# #!/bin/sh
# sudo -i -u skype /home/skype/sevabot/scripts/check-service.sh
#
# chmod u+x /etc/cron.hourly/check-seva

# http://stackoverflow.com/a/246128/315168
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HELPER=$DIR/start-server.sh

REBOOT=$DIR/reboot-seva.sh

$HELPER status

# Non-zero return code means one of Sevabot underlying services has gone MIA
if [ "$?" != "0" ] ; then
    $REBOOT
fi
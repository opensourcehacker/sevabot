#!/bin/bash
#
# Control sevabot and related services.
#
# This script is not multi-user safe... use for single UNIX user "skype" server deployments only.
#
# As this script has lived through ages and have never seen a clean rewrite, it's ugly
# and direly needs something better to upgrade it. Replace it with supervisord:
#
# http://supervisord.org/
#
# The orignal script by mweber at http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/
#
#

DAEMON_USER=skype
XSERVERNUM=1

export DISPLAY=:$XSERVERNUM

dnb=`dirname "$0"`

#: Sevabot script location
seva=`dirname "$0"`/../venv/bin/sevabot

# Which services we are
services="$SERVICES"
if [[ -z "$services" ]]
then
    services="xvfb fluxbox skype sevabot"
fi

# On OSX we need to force 32-bit compatiblity
if [[ "$OSTYPE" == "darwin" ]] ; then
    seva="arch -i386 $seva"
fi

start() {


    if [[ $services == *xvfb* ]]
    then
        if [[ `ps aux | grep "$DAEMON_USER" | grep "Xvfb :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then
                echo "starting Xvfb"
                Xvfb :$XSERVERNUM -screen 0 800x600x16 &
        else
                echo "Xvfb already running"
        fi
    fi

    if [[ $services == *fluxbox* ]]
    then
        if [[ `ps aux | grep "$DAEMON_USER" | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
                echo "starting fluxbox"
                sleep 3
                fluxbox &
        else
                echo "fluxbox already running"
        fi
    fi

    if [[ $services == *skype* ]]
    then
        pgrep skype > /dev/null
        if [[ $? != '0' ]]; then
            sleep 3
            #  http://devforum.skype.com/t5/Audio-Video/bt-audio-service-open-connect-failed-Connection-refused-111/td-p/303
            skype > /dev/null 2&>1 &
        else
            echo "skype already running"
        fi
    fi

    if [[ $services == *sevabot* ]]
    then
        pgrep -f venv/bin/sevabot > /dev/null
        if [[ $? == '0' ]] ; then
            echo "Sevabot already running"
        else
            # this sleep prevents skype.Attach() from failing
            sleep 3
            $seva --daemon > /dev/null
            echo "Started Sevabot web server process id $!"
        fi
    fi
}

stop() {

    if [[ $services == *skype* ]]
    then
        pgrep skype > /dev/null
        if [[ $? != '0' ]]; then
            echo "skype is NOT running"
        else
            echo "killing skype"
            killall skype
        fi
    fi

    if [[ $services == *fluxbox* ]]
    then
        if [[ `ps aux | grep "$DAEMON_USER" | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
            echo "fluxbox is NOT running"
        else
            echo "Killing fluxbox"
            killall fluxbox
            sleep 3
            killall -SIGKILL fluxbox
        fi
    fi


    if [[ $services == *xvfb* ]]
        then
        if [[ `ps aux | grep skype | grep "Xvfb :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then
            echo "Xvfb is NOT running"
        else
            echo "Killing Xvfb"
            killall Xvfb
        fi
    fi


    if [[ $services == *sevabot* ]]
    then
        pgrep -f venv/bin/sevabot > /dev/null
        if [[ $? != '0' ]] ; then
            echo "Sevabot not running"
        else
            pkill sevabot
        fi
    fi
}

status() {

    i='4'


    if [[ $services == *xvfb* ]]
    then
        if [[ `ps aux | grep "$DAEMON_USER" | grep "Xvfb :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then
            echo "Xvfb is NOT running"
        else
            echo "Xvfb is running"
            ((i--))
        fi
    else
        ((i--))
    fi

    if [[ $services == *fluxbox* ]]
    then
        if [[ `ps aux | grep "$DAEMON_USER" | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
            echo "fluxbox is NOT running"
        else
            echo "fluxbox is running"
            ((i--))
        fi
    else
        ((i--))
    fi

    if [[ $services == *skype* ]]
    then
        pgrep skype > /dev/null
        if [[ $? != '0' ]]; then
            echo "skype is NOT running"
        else
            echo "skype is running"
            ((i--))
        fi
    else
        ((i--))
    fi

    if [[ $services == *sevabot* ]]
    then
        pgrep -f venv/bin/sevabot > /dev/null
        if [[ $? == '0' ]] ; then
            echo "Sevabot running"
            ((i--))
        else
            echo "Sevabot NOT running"
        fi
    else
        ((i--))
    fi

    if [[ "$i" == '0' ]]; then
        echo "OVERALL STATUS: OK"
        exit 0
    fi
    if [[ "$i" == '1' || "$i" == '2' ]]; then
        echo "OVERALL STATUS: NOT RUNNING PROPERLY"

    else
        echo "OVERALL STATUS: NOT RUNNING"
    fi
    exit "$i"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Example to start everything till sevabot:"
        echo ""
        echo "scripts/start-server.sh start"
        echo ""
        echo "Example to start Xvfb, Fluxbox and Skype needed to install sevabot"
        echo ""
        echo "SERVICES='xvfb fluxbox skype' scripts/start-server.sh start"
        exit 1
esac

#!/bin/bash

##
# Script by mweber at http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/
##

DAEMON_USER=skype
XSERVERNUM=1

if [[ "$USER" != "$DAEMON_USER" ]]; then
    echo "Please start this script as $DAEMON_USER!"
    exit 1
fi


export DISPLAY=:$XSERVERNUM

dnb=`dirname "$0"`

start() {
    SERVICES='xvfb fluxbox skype' "$dnb/start-server.sh" status
    if [[ "$?" == '0' ]]; then
        echo "Starting x11vnc"
        if [[ `ps aux | grep "$DAEMON_USER" | grep "x11vnc -display :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then

            install -d ~/.x11vnc
            if [[ ! -e ~/.x11vnc/passwd ]]
            then
                # Set the default password
                x11vnc -storepasswd ~/.x11vnc/passwd
            fi

            x11vnc -display :$XSERVERNUM -bg -xkb -rfbauth ~/.x11vnc/passwd
        else
            echo "x11vnc is already running!"
        fi
        echo "----------------------------------------------------------------------------------------"
        echo "Now connect to this server from your local computer using VNC remote desktop viewer"
        echo "----------------------------------------------------------------------------------------"
    else
        echo "The server doesn't run."
        echo 'Use "'"$dnb"'/start-server.sh" to start the server'
    fi

}


status() {
    if [[ `ps aux | grep "$DAEMON_USER" | grep "x11vnc -display :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then
        echo "x11vnc isn't running"
        exit 1
    else
        echo "x11vnc is running"
        exit 0
    fi
}

stop() {
    if [[ `ps aux | grep "$DAEMON_USER" | grep "x11vnc -display :$XSERVERNUM" | grep -v grep | wc -l` == '0' ]]; then
        echo "x11vnc isn't running"
    else
        echo "killing x11vnc"
        killall x11vnc
    fi
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
        exit 1
esac

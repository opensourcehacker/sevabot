#!/bin/bash

##
# Script by mweber at http://www.qxs.ch/2011/01/07/skype-instant-messages-from-zabbix/
##

if [[ "$USER" != 'skype' ]]; then
	echo "Please start this script as skype!"
	exit 1
fi

export DISPLAY=:1

dnb=`dirname "$0"`


start() {
	"$dnb/start-server.sh" status
	if [[ "$?" == '0' ]]; then
		echo "Starting x11vnc"
		if [[ `ps aux | grep skype | grep "x11vnc -display :1" | grep -v grep | wc -l` == '0' ]]; then
		x11vnc -display :1 -bg -nopw -listen localhost -xkb
		else
			echo "x11vnc is already running!"
		fi
		#pid=`ps aux | grep skype | grep "x11vnc -display :1" | grep -v grep | awk '{ print $2; }'`
		echo "	now use on your machine: ssh -L 5900:127.0.0.1:5900 'skype@`hostname`'"
		echo "	and connect to your local port with vncviewer!"
	else
		echo "The server doesn't run."
		echo 'Use "'"$dnb"'/start-server.sh" to start the server'
	fi
	
}


status() {
	if [[ `ps aux | grep skype | grep "x11vnc -display :1" | grep -v grep | wc -l` == '0' ]]; then
		echo "x11vnc isn't running"
		exit 1
	else
		echo "x11vnc is running"
		exit 0
	fi
}

stop() {
	if [[ `ps aux | grep skype | grep "x11vnc -display :1" | grep -v grep | wc -l` == '0' ]]; then
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

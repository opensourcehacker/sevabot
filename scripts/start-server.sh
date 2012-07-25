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
	if [[ `ps aux | grep skype | grep "Xvfb :1" | grep -v grep | wc -l` == '0' ]]; then
		echo "starting Xvfb"
		Xvfb :1 -screen 0 800x600x16 &
	else
		echo "Xvfb already running"
	fi
	if [[ `ps aux | grep skype | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
		echo "starting fluxbox"
		sleep 1
		fluxbox &
	else
		echo "fluxbox already running"
	fi
	if [[ `ps -eo pid,user,args | grep skype | awk '{ print $1 " " $3; }' | grep skype | wc -l` == '0' ]]; then
		echo "starting skype"
		sleep 2
		skype &
	else
		echo "skype already running"
	fi
}

stop() {
	if [[ `ps -eo pid,user,args | grep skype | awk '{ print $1 " " $3; }' | grep skype | wc -l` == '0' ]]; then
		echo "skype is NOT running"
	else
		echo "killing skype"
		killall skype
	fi

	"$dnb/start-vnc.sh" stop

	if [[ `ps aux | grep skype | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
		echo "fluxbox is NOT running"
	else
		echo "Killing fluxbox"
		killall fluxbox
	fi
	if [[ `ps aux | grep skype | grep "Xvfb :1" | grep -v grep | wc -l` == '0' ]]; then
		echo "Xvfb is NOT running"
	else
		echo "Killing Xvfb"
		killall Xvfb
	fi
}

status() {
	i='3'
	if [[ `ps aux | grep skype | grep "Xvfb :1" | grep -v grep | wc -l` == '0' ]]; then
		echo "Xvfb is NOT running"
	else	
		echo "Xvfb is running"
		((i--))
	fi
	if [[ `ps aux | grep skype | grep "fluxbox" | grep -v grep | wc -l` == '0' ]]; then
		echo "fluxbox is NOT running"
	else
		echo "fluxbox is running"
		((i--))
	fi
	if [[ `ps -eo pid,user,args | grep skype | awk '{ print $1 " " $3; }' | grep skype | wc -l` == '0' ]]; then
		echo "skype is NOT running"
	else
		echo "skype is running"
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
exit 1
esac

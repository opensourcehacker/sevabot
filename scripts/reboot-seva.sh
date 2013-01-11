#!/bin/bash
#
# A script to restart everything in Sevabot under skype UNIX user.
# Assumes Ubunutu + headless Sevabot installation.
#
# Assumes sevabot is installed in ~/sevabot and virtualenv in ~/sevabot/venv
#
# Add the following entry in your SSH config:
#
# Host sevabot
# User skype
# Hostname example.com
# ForwardAgent no
#
# More SSH info http://opensourcehacker.com/2012/10/24/ssh-key-and-passwordless-login-basics-for-developers/
#
# To make sevabot launch on the server reboot add the following line in /etc/rc.local
#
# sudo -i -u skype /home/skype/sevabot/scripts/reboot-seva.sh


cd ~/sevabot

# Assume sevabot has been cloned under ~/sevabot

# Restart Xvfb + Skype
scripts/start-server.sh stop

sleep 5 # Need some delay as xvfb dying might take a while

#
# Comment SSH part out if your bot scripts don't use SSH
#

# Run ssh-add only if the terminal is in interactive mode
# http://serverfault.com/questions/146745/how-can-i-check-in-bash-if-a-shell-is-running-in-interactive-mode
# OK, this is really lame to assume xterm but could not find other reliable
# way to detect run from /etc/rc.local (which sets terminal to linux)
if [[ "$TERM" == "xterm" ]]
then
    if [ -n "$SSH_AUTH_SOCK" ] ; then
        echo "Cannot add a local user SSH key when SSH agent forward is enabled"
        exit 1
    fi

    # Restart sevabot in screen
    eval `ssh-agent`

    # For the security reasons we do not store the
    # SSH key on the server as bot scripts have root access to some systems
    echo "Please give SSH key passphase needed by the sevabot scripts"

    ssh-add
fi

scripts/start-server.sh start > /dev/null 2>&1

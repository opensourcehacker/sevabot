#!/bin/sh
#
# A script to restart everything in Sevabot under skype UNIX user.
# Assumes Ubunutu + headless Sevabot installation.
#
# Assumes sevabot is installed in ~/sevabot and virtualenv in ~/sevabot/venv
#
cd ~/sevabot

# Activate virtualenv
. venv/bin/activate

# Assume sevabot has been cloned under ~/sevabot

# Restart Xvfb + Skype
scripts/start-server.sh stop

sleep 5 # Need some delay as xvfb dying might take a while

scripts/start-server.sh start

# Use Xvfb X display to run Skype
export DISPLAY=:1

#
# Comment SSH part out if your bot scripts don't use SSH
#

# Restart sevabot in screen
eval `ssh-agent`

# For the security reasons we do not store the
# SSH key on the server as bot scripts have root access to some systems
echo "Please give SSH key passphase needed by the sevabot scripts"

ssh-add

#
# ... and now continue with starting
#

# KIll existing screen instances, kills also danling sevabot instances
pkill -f "Sevabot screen"

# Create a named screen instance which will leave the bot Python daemon running
# You can later attach this with screen -x
# Note: If you are trying to start via sudo
# you mught need to do this first to fix screen:
# script /dev/null

screen -dm -t "Sevabot screen" sevabot

echo "Sevabot is now running in screen"
echo "Type screen -x to attach and see the bot logs"





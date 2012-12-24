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
scripts/start-server.sh restart

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
DISPLAY=:1 screen -t "Sevabot screen" sevabot





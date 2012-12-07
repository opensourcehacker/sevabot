#!/bin/bash
#
# Run CI check for every 5 minutes and
# execute tests if svn has been updated.
#
# The script sets up xvfb (X window framebuffer)
# which is used to run the headless Firefox.
#
# We will post a Skype message if the Selenium WebDriver
# has some issues (it often hangs)
#
# We also signal the tests to use a special static Firefox build
# and do not rely (auto-updated) system Firefox
#
# NOTE: This script is NOT sh compliant (echo -n),
# bash needed

# Timeouting commands shell script helper
# http://stackoverflow.com/a/687994/315168
TIMEOUT=timeout.sh

# Which FF binary we use to run the tests
FIXED_FIREFOX=$HOME/ff16/firefox/firefox

# It's me, Mariooo!
SELF=$(readlink -f "$0")

# Skype endpoint information
SKYPE_CHAT_ID="1234567890"

SKYPE_SHARED_SECRET="toholampi"

SEVABOT_SERVER="http://yourserver.com:5000/msg/"

#
#  Helper function to send Skype messages from help scripts.
#  The messages are signed with a shared seceret.
#
#  Parameter 1 is the message
#
function send_skype_message() {
    msg="$1"
    md5=`echo -n "$SKYPE_CHAT_ID$msg$SKYPE_SHARED_SECRET" | md5sum`

    #md5sum pads a '-' to the end of the string. We need to get rid of that.
    for m in $md5; do
        break
    done

    result=`curl --silent --data-urlencode chat="$SKYPE_CHAT_ID" --data-urlencode msg="$msg" --data-urlencode md5="$m" $SEVABOT_SERVER`
    if [ "$result" != "OK" ] ; then
        echo "Error in HTTP communicating to Sevabot: $result"
    fi
}

# Tell the tests to use downgraded FF!6
# which actually works with Selenium
if [ -e $FIXED_FIREFOX ] ; then
    FIREFOX_PATH=$FIREFOX_PATH
    export FIREFOX_PATH
    echo "Using static Firefox 16 build to run the tests"
fi

send_skype_message "♫ ci-loop.sh restarted at $SELF"

while true
do
    # Kill hung testing processes (it might happen)
    pkill -f "bin/test"

    # Purge existing xvfb just in case
    pkill Xvfb

    sleep 5

    echo "Opening virtual X11"

    # Start headless X
    Xvfb :15 -ac -screen 0 1024x768x24 &

    # Tell FF to use this X server
    export DISPLAY=localhost:15.0

    # Run one cycle of continous integration,
    # give it 15 minutes to finish
    echo "Starting test run"
    $TIMEOUT -t 900 continous-integration.sh
    result=$?

    if [ "$result" == "143" ] ; then
        echo "------- CI TIMEOUT OOPS --------"
        send_skype_message "⚡ Continuous integration tests timed out - check the ci-loop.sh screen for problems"
    fi

    sleep 300
done
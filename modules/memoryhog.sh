#!/bin/sh

# I's best to use ssh-agent and .ssh/config for this.

HOST=$1

if [ -z "$HOST" ]; then
    echo "Usage: !memoryhog <host or all>"
elif [ "$HOST" = "all" ]; then
    HOSTS=`grep "Host " ~/.ssh/config | awk '{print $2}'`

    for h in $HOSTS; do
        echo -n "$h: "
        ssh $h "ps -eo vsize,args --sort vsize | tail -n 1"
    done

else
    ssh $HOST "ps -eo vsize,args --sort vsize | tail -n 1"
fi

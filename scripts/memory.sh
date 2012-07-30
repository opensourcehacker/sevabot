#!/bin/sh

highest=`ps -eo vsize,comm --sort vsize | tail -n 1`

set -- $highest

mem=$1

if [ "$mem" -gt "1228800" ]; then
    echo $highest
fi

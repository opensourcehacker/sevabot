#!/bin/sh

ssh $1 "ps -eo vsize,args --sort vsize | tail -n 1"
#!/bin/sh

ssh $1 "ps -eo vsize,comm --sort vsize | tail -n 1"
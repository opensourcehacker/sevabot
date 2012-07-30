#!/bin/sh

echo `ps -eo vsize,comm --sort vsize | tail -n 1`
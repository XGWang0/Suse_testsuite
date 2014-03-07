#!/bin/bash

echo "$1 $@"
date '+%H-%M-%S'
echo 'In Development' > /var/log/qa/ctcs2/sq-perf-fake-log
sleep 180
date '+%H-%M-%S'
echo "I am quiting"

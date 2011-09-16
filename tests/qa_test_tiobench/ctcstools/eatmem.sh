#!/bin/bash

totalmem=`cat /proc/meminfo | grep MemTotal | sed -e 's/MemTotal:\W*//g' -e 's/ kB//'`
eatmem $totalmem 512

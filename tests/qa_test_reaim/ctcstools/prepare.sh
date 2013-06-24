#!/bin/bash
DIR=`grep DISKDIR /usr/lib/ctcs2/config/reaim/reaim.config|cut -d " "  -f 2`
if ! [ -d $DIR ]
then
	mkdir -p $DIR
fi

#!/bin/bash

# qa_slepos-config

# File:		defaults.sh 

# Author:	Tomas Cech <tcech@suse.cz>

# Description:	This file contains configuration, which will
#		be used for this tests and some common functions.

#		!!! exporting of variables is important - it's used for expect scripts !!!

. "$CONF_PATH/defaults.sh"

# by setting this number you select, in which location will this branch server be
location_number=1

# external IP address of new branch server
# set IP address, if you have more than one different address from 127.0.0.1 and $internal_ip
# if it is only one, it will use it

#ip="192.168.0.115"

# IP address of internal network of the new branch server
internal_ip="192.168.123.1"

# network device of internal network
##device=eth0
device=eth0

# branch server name - must be set the same way on branch server...
scBranchServer=citharacanthus

# loading location specific settings
. "$CONF_PATH/location${location_number}.sh"

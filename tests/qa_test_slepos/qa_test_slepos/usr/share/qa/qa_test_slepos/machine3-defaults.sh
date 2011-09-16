#!/bin/bash 

# qa_slepos-config

# File:		machine1-defaults.sh 

# Author:	Tomas Cech <tcech@suse.cz>

# Description:	This file contains definition of some machine, which will
#		be used for this tests and some common functions.
#		It is in global part of LDAP.

# configuration settings

cr="default_CR"
cr_name="default"
scPosImageDn="cn=minimal,cn=default,cn=global,o=${organization},c=${country}"
disk_type="disk"
disk_device="/dev/sda"
disk_device_name="sda"
if [ "$pos_version" -lt 11 ]; then
        disk_device="/dev/hda"
        disk_device_name="hda"
else
        disk_device="/dev/sda"
        disk_device_name="sda"
fi
disk_size="5000"
disk_partitioning="1000 82 swap swap;3000 83 / ext3;"

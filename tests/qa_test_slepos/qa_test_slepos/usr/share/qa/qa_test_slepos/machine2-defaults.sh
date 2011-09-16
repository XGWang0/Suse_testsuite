#!/bin/bash 

# qa_slepos-config

# File:		machine2-defaults.sh 

# Author:	Tomas Cech <tcech@suse.cz>

# Description:	This file contains definition of some machine, which will
#		be used for this tests and some common functions.
#		It is in global part of LDAP.

# configuration settings

cr="round_cr"
cr_name="Round Beauty 3000"
scPosImageDn="cn=graphical,cn=default,cn=global,o=${organization},c=${country}"
disk_type="ramdisk"
disk_device="/dev/ram1"
disk_device_name="ram"

#not used for ramdisk
#disk_size="5000"
#disk_partitioning="1000 82 swap swap;3000 83 / ext3;"

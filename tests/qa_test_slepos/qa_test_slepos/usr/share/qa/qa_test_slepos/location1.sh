#!/bin/bash 

# qa_slepos-config

# File:		defaults.sh 

# Author:	Tomas Cech <tcech@suse.cz>

# Description:	This file contains configuration, which will
#		be used for this tests and some common functions.

#		!!! exporting of variables is important - it's used for expect scripts !!!


############################ You probably don't need to change this configuration ###########################################

# this number specifies, in which organizational unit this location belongs to
organizational_unit_number=1

# location name - for example shop_wall_street
scLocation=GrandKanal

# container common name
scServerContainer=kontejner


# gateway of location
##gateway="192.168.0.1"
gateway="192.168.123.1"

# local network, where is branch server and cash register (POS) machines
network="192.168.123.0"
mask="255.255.255.0"

# range of adresses for DHCP in local network of branch server
DhcpRange1="192.168.123.10"
DhcpRange2="192.168.123.50"

# range of fixed adresses for DHCP in local network of branch server
DhcpFixedRange1="192.168.123.51"
DhcpFixedRange2="192.168.123.151"
# base name, which will be used for newly connected cash register machines (POS)
WorkstationBaseName=CR
# this mask will be appended to base name
EnumerationMask=00
# for:
# WorkstationBaseName=CR
# EnumerationMask=00
# first connected machine CR01, next CR02, CR03 ...


DynamicIP=TRUE

# use external DHCP server? (SLEPOS >= 10 only)
dhcpExtern=FALSE

# if dhcpExtern is TRUE these values are used

# machines where DHCP runs
ExtDHCP_machine=scruffy

# interface where DHCP runs
ExtDHCP_interface=eth1

# IP4 range for external DHCP
# ExtDHCP_range_min .. ExtDHCP_range_max
ExtDHCP_range_min=192.168.122.10
ExtDHCP_range_max=192.168.122.40

# default lease time
ExtDHCP_default_time=20000
# max lease time
ExtDHCP_max_time=20000

# introduced in SLEPOS11: this new attribute is --userPassword "branchpass"

userPassword='kkt'

if false; then
# I want to use local settings
scDnsDn="`sed -n '/nameserver/s/nameserver //p' /etc/resolv.conf | head -n 1`"
# but not if it is set to localhost
if [ "$scDnsDn" = 127.0.0.1 ]; then
	unset scDnsDn
fi

fi #false

# loading organizational unit configuration
. "$CONF_PATH/organizational_unit${organizational_unit_number}.sh"

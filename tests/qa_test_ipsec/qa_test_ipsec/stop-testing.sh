#!/bin/bash

DIR=$(dirname `readlink -f $0`)
. $DIR/testing.conf
. $DIR/scripts/function.sh

echo "Stopping test environment"

NETWORKS="vnet1 vnet2 vnet3"

check_commands virsh

for net in $NETWORKS
do
	log_action "Network $net"
	execute "virsh net-destroy $net"
done

for host in $STRONGSWANHOSTS
do
	log_action "Guest $host"
	execute "virsh shutdown $host"
#	rm -f $VIRTIMGSTORE/$host.$IMGEXT
done


#!/bin/bash
rm -rf ~/.evolution/ ~/.gconf/apps/evolution/ ~/.gnome2_private/*

gconfd_pid=`ps -ef |grep "gconfd-2" |grep -v grep |awk '{print $2}'`

if [ "$gconfd_pid" ] && [ "$USER" == "root" ]; then
	killall gconfd-2
else
	user_pid=`ps -ef |grep "gconfd-2" |grep -v grep |grep -v "root" |awk '{print $2}'`
	if [ "$user_pid" ]; then
		kill $user_pid
	fi
fi

gkd_pid=`ps -ef |grep "gnome-keyring-daemon" |grep -v grep |awk '{print $2}'`
if [ "$gkd_pid" ]; then
	killall gnome-keyring-daemon
fi


#
# Small shell script that prepares enviroment for openssh tests.
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

#!/bin/sh

# path to the directory for temporary test files
export LC_ALL=C
WORKING_PATH=/tmp/qa_test_openssh
mkdir -p $WORKING_PATH || exit 1
chown -R nobody $WORKING_PATH

# get path to ssh binaries
export TEST_SSH_SSH=`which ssh`
export TEST_SSH_SSHD=`which sshd`
export TEST_SSH_SSHAGENT=`which ssh-agent`
export TEST_SSH_SSHADD=`which ssh-add`
export TEST_SSH_SSHKEYGEN=`which ssh-keygen`
export TEST_SSH_SSHKEYSCAN=`which ssh-keyscan`
export TEST_SSH_SFTP=`which sftp`
export TEST_SSH_SCP=`which scp`
export TEST_SSH_SFTPSERVER=`grep sftp-server /etc/ssh/sshd_config | awk '{print $3}'`

if ! ( [[ "$1" =~ "transfer.sh" ]] || [[ "$1" =~ "rekey.sh" ]] ); then
        export TEST_SSH_SSH="$TEST_SSH_SSH -n"
fi

SFTP_SERVER_PATH_OPTION='-D'
MAJOR=`rpm -qi openssh| awk '/Version/{print $3}'| sed  -r 's/([0-9]+)\.([0-9]+).*/\1/'`
MINOR=`rpm -qi openssh| awk '/Version/{print $3}'| sed  -r 's/([0-9]+)\.([0-9]+).*/\2/'`

#if (( $MAJOR >= 5 && $MINOR >= 4)) 
if (( $MAJOR > 5 )) 
then
	export SFTP_SERVER_PATH_OPTION='-D'
elif (( $MAJOR == 5))
then
    if (( $MINOR >=4 ))
    then 
	export SFTP_SERVER_PATH_OPTION='-D'
    else
	export SFTP_SERVER_PATH_OPTION='-P'
    fi
else
	export SFTP_SERVER_PATH_OPTION='-P'
fi



# set environment
export SUDO=sudo
export TEST_SHELL=/bin/sh
export TEST_SSH_LOGFILE=${WORKING_PATH}/qa_openssh.log

# add directory witch stores testscripts into PATH
if `echo $PATH |grep /usr/share/qa/qa_openssh &> /dev/null`; then 
	true;
else 
	PATH=$PATH:/usr/share/qa/qa_test_openssh/ 
fi

EXIT_CODE=0

# enable sudo without password
SUDO_TEMPFILE="`mktemp`"
cp /etc/sudoers $SUDO_TEMPFILE
chmod 440 $SUDO_TEMPFILE
echo 'nobody	ALL=(ALL)	NOPASSWD: ALL' >> /etc/sudoers

# exec test name $1
su nobody -c "sh test-exec.sh $WORKING_PATH $1" || EXIT_CODE=1

# clean after test
rm -rf $WORKING_PATH

# disable sudo without password
mv $SUDO_TEMPFILE /etc/sudoers

exit $EXIT_CODE

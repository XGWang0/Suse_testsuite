#!/bin/bash
DATA_DIR="/usr/share/qa/qa_test_multipath/data"
DTOPT="iotype=random capacity=2g flags=sync,rsync limit=1g enable=lbdata,raw min=b max=256k incr=var dlimit=512 oncerr=abort dtype=disk passes=inf"
#Load external vars
. $DATA_DIR/vars

if [ "HW" = "1" ];then
trap 'stop_data;cleanup;restore_conf' EXIT SIGHUP SIGINT SIGTERM
else
trap 'stop_data;cleanup;iscsi_disconnect;restore_conf' EXIT SIGHUP SIGINT SIGTERM
fi
#get SLE version
CODE=`cat /etc/SuSE-release | awk -F "=" '/VERSION/''{ print $2 }'\
        | cut -c 2-3`
SP=`cat /etc/SuSE-release | awk -F "=" '/PATCHLEVEL/''{ print $2 }'\
        | cut -c 2`

if [ $CODE -eq 11 ]; then
        PART="_part1"
fi
if [ $CODE -eq 10 ]; then
        PART="-part1"
fi

if [ -z $TARGET ];then
        echo "target address is not set. Please define TARGET variable"
        exit 5;
fi
if [ -z $TARGET_DISK ];then
        echo "target disk is not set. Please define TARGET_DISK variable"
        exit 5;
fi
if [ -z $PART_SIZE ];then
        echo "PART_SIZE is not set. Please define PART_SIZE variable"
        exit 5;
fi


#get device name
function get_paths ()
{
if [ $CODE -eq 11 -a $SP -eq 1 ];then
PATHS=( "" `multipathd -k"list map $map topology"|sed -n '/[0-9]:[0-9]/ p'|cut -c 2- | awk -F " " '{print $3}'`)
else
PATHS=( "" `multipathd -k"list map $map topology"|sed -n '/[0-9]:[0-9]/ p'| cut -d " " -f 4`)
fi
}

#get device status
function paths_status ()
{
PATHS_STATUS=( "" `multipathd -k"list map $map topology"|sed -n '/[0-9]:[0-9]/ p'| sed -r 's/.*(active|failed|enabled).*/\1/'`)
}

#fail path
function fail_path ()
{
echo "offline" > /sys/block/${PATHS[$1]}/device/state
}

#recover path
function recover_path ()
{
echo "running" > /sys/block/${PATHS[$1]}/device/state
}

#I/O
function copy_data () 
{
	echo "do I/O"
	startproc -q /usr/bin/dt of=/mnt/$map/test_data pattern=iot $DTOPT
	DATA_PID=$(checkproc -v /usr/bin/dt)
}

function stop_data ()
{
	killproc /usr/bin/dt
}
function check_data () {
	if $(checkproc /usr/bin/dt);then
        echo "PASSED: data flow is ok"
        return 0;
	else
	return 1;
        fi
}
function check_active {
	echo "path ${PATHS[$1]} is ${PATHS_STATUS[$1]}"
	if [ ${PATHS_STATUS[$1]} = "active" ];then
	return 0;
	else 
	return 1;
	fi
}

function check_failed {
	echo "path ${PATHS[$1]} is ${PATHS_STATUS[$1]}"
        if [ ${PATHS_STATUS[$1]} = "failed" ];then
        return 0;
        else 
        return 1;
        fi
}
#clean-up
function cleanup () 
{
        echo "cleanup"
        cat /proc/mounts | grep $map$PART && umount /dev/mapper/$map$PART
	rm -rf /mnt/$map
	parted -s /dev/mapper/$map rm 1
	udevsettle
        multipath -f $map
}

function iscsi_disconnect () 
{
        iscsiadm -m node -T $TARGET_DISK -u
}

function iscsi_connect ()
{
        /etc/init.d/open-iscsi status
        if [ $? -ne 0 ]; then
                /etc/init.d/open-iscsi start
        fi
        echo "reset already discovered target"
        iscsiadm -m node | grep $TARGET_DISK 
        if [ $? -eq 0 ];then
        iscsiadm -m node -T $TARGET_DISK -u
        iscsiadm -m node -T $TARGET_DISK -o delete
        if [ $? -ne 0 ]; then
              echo " delete failed"
                exit 1;
        fi
        fi
        echo "bind target"
        iscsiadm -m node -T $TARGET_DISK -p $TARGET -o new
        if [ $? -ne 0 ]; then
              echo "bind failed"
                exit 1;
        fi

        echo "connect target"
        iscsiadm -m node -T $TARGET_DISK -l
        if [ $? -ne 0 ]; then
              echo "connect failed"
                exit 1;
        fi
	echo "iSCSI connected"
}

config_prepare ()
{
#Get LUNS attached to system
CONF=$(mktemp /tmp/mpath.confXXX)
DEV_MAPS=$(mktemp /tmp/map.XXX)

if [ -f /etc/multipath.conf ];then
	cat /etc/multipath.conf | grep -F "user_friendly_names yes"
	if [ $? -eq 0 ];then
	multipath -ll | egrep '[0-9a-z]{32}' | sed -e 's/dm\-[0-9]//g' -e 's/,/\ /g' -e 's/(//g' -e 's/)//g' -e 's/^ *[^ ]* //' > "$CONF"
	fi
else
	multipath -ll | grep '^[0-9]'| sed -e 's/dm\-[0-9]//g' -e 's/,/\ /g' > $CONF
fi
if [ $(grep -c "$1" "$CONF") -eq 0 ];then
	return 50;
fi
grep "$1" $CONF > $DEV_MAPS
N=1
cat << EOF > /etc/multipath.conf
defaults {
    user_friendly_names yes 
    max_fds max
}
multipaths {
EOF

while read map;
	do
        ALIAS=$(echo $map| awk -F ' ' '{OFS = "-"; print $2, $3}')
        WWID=$(echo $map| awk -F ' ' '{print $1}')
	cat << EOF >> /etc/multipath.conf
    multipath {
        wwid $WWID 
        alias $ALIAS-$N
    }
EOF
	MAPS=( "${MAPS[@]}" "$ALIAS-$N" )
	N=`expr $N + 1`
done < $DEV_MAPS
echo "}" >> /etc/multipath.conf
rm $CONF
rm $DEV_MAPS
}
function prepare () 
{
	if [ "$HW" != "1" ];then
		if [ ! -z "$CONFIG" ];then 
			cp $CONFIG /etc/multipath.conf 
		fi
	fi
        /etc/init.d/multipathd status
        if [ $? -ne 0 ]; then
                /etc/init.d/multipathd restart

                if [ $? -ne 0 ]; then
                echo "multipathd start FAILED"
                exit 1;
                fi
        fi

	#multipathd -k"reconfigure"
	multipath -v2
	udevsettle
        echo "create fs"
        parted -s /dev/mapper/$map mklabel msdos
        parted -s /dev/mapper/$map mkpart primary 0 $PART_SIZE
	udevsettle
        if [ $CODE -eq 10 ];then
        kpartx -a -p -part /dev/mapper/$map
	udevsettle
        fi
        if [ ! -f /mnt/$map ]; then
        mkdir -p /mnt/$map
        fi
	mkfs.reiserfs -q /dev/mapper/$map$PART
        mount /dev/mapper/$map$PART /mnt/$map
        if [ $? -ne 0 ]; then
              echo "mount failed"
                exit 1;
        fi
        echo "Initial setup done"
}

function backup_conf () {
if [ -f /etc/multipath.conf ];then
   tar -czf $BACKUP -C / /etc/multipath.conf 2> /dev/null || exit 2
fi
}
function restore_conf () {
if [ -f $BACKUP ];then
   tar -xzf $BACKUP -C / 2> /dev/null || exit 2
   rm $BACKUP
fi
}

function reseterr() {
	ERRORS=0;
	SCRIPTERR=0;
}

function checkerror() {
	if [ $? -ne 0 ]; then
        	ERRORS=$(( $ERRORS + 1 ))
		echo -e "\tERROR occured"
	else
		echo -e "\tOK"
	fi
}

function checkscript() {
        if [ $? -ne 0 ]; then
                SCRIPTERR=$(( $SCRIPTERR + 1 ))
                echo -e "\tSCRIPT ERROR occured"
        else
                echo -e "\tOK"
        fi
}


function getwd() {
	CWD=`pwd`
}


function createresult() {
	if [ $ERRORS -ne 0 ]; then
        	echo FAILED
        	exit 1
	else
        	echo PASSED
        	exit 0
	fi
}


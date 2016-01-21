#!/bin/bash
#
#
# Feature request:
# - Check whether backup logs in /var/log/qaset/log/
#   +  yes: launch script to submit logs to QADB one by one
#   +  no: exit 
#

backup_logdir="/var/log/qaset/log/"
default_logdir="/var/log/qa/ctcs2/"

#  ============   START  aux functions  ==============
#

function usage() {
        echo "
Usage:   $0 [-h] [-B backupdir] [-q database] [-t testsuite name]
            [-a all of logs] [-f logdir] [-o remote_qa_db_report.pl options]

            to sibmit the logs in backup log directory  on this host
            to QADB or other database.

Options:
         -B   Specify the backup directory(default: $default_workdir)
         -h   Print this help text and exit successfully
         -q   Specify the database 
	      (default is the same with /etc/qa/0-qa_tools-default remote_qa_db_report_host,parameter "de" or "cn")
         -t   Specify the log name want to submit
              Default: -a (submit all of logs in backup directory)
         -a   Submit all of logs in backup dir to database
         -f   logs directory
         -o   options of /usr/share/qa/tools/remote_qa_db_report.pl 
              ([ -p PRODUCT] [-c <comment>] [-b] [-L] [-D] [-A] [-v <n>] 
               [-a ARCH] [-N BUILD_NUMBER ] [-f PATH] [-F TCF_LIST] 
               [-P DIRECT_PATH_LIST]  [-k KERNEL] [-m TESTHOST] 
               [-t TYPE] [-T TESTER] 
               details run /usr/share/qa/tools/remote_qa_db_report.pl -h)
"    
    return 0
}

#database=`grep "^remote_qa_db_report_host=" /etc/qa/00-qa_tools-default | awk -F"=" '{print $2}'`
testsuite="a"
remote_script_opts=""
while getopts hB:q:o:t:a optchar ; do

    case "$optchar" in

      h)      usage
              exit 0                            ;;
      B)      backup_logdir=$OPTARG             ;;
      q)      database=$OPTARG                  ;;
      o)      remote_script_opts=" $OPTARG"     ;;
      t)      testsuite=$OPTARG                 ;;
      a)      testsuite="a"                     ;;
      f)      default_logdir=$OPTARG            ;;
      *)      usage
              exit "$exitcode" ;;
    esac
done
shift $((OPTIND - 1))

#   =================  Preparation  =================
#
#find usable log directory
for A in  $backup_logdir $default_logdir
do
    if [ -d $A ]
    then
        echo "$A is exist!"
    fi
done


if test -z "$testsuite";then
   testsuite='a' 
fi

#
#   ====  END Preparation ===============================

function decompresslog {
    cd $backup_logdir
    logname=$1
    for log in `ls $backup_logdir |grep $logname`;do
        tar -xvf $log 
        if test $? -eq 0;then
            dn=`tar -tf $log |sed 'q'`		
            mv $dn  $default_logdir
        else
            echo "Decompress $log failed!"
	    return 1
        fi
    done
    return 0
}

function submitalllogs {
    failedlogs=`grep "\[qadb\] [a-z_1-9]* submit qa_db_report failed\!" /var/log/qaset/calls/* | awk '{print $4}'`
    for log in $failedlogs;do 
        submitonelog "$log"
    done
}

function submitonelog {
    logname=$1
    decompresslog "$logname"
    if test $? -eq 0;then
        submitlog "$logname"
    else
        sq_error "Decompress some of tar package failed!"
    fi
}

function getconfig {
    if ip -4 addr | grep "inet 147\.2\." > /dev/null;then
        SQ_HOSTNAME=$(hostname).apac.novell.com
    else
        SQ_HOSTNAME=$(hostname)
    fi
    comment=`ls $default_logdir |sed 'q'`
}

run_id=""

function submitlog {
    logname=$1
    if test -z $remote_script_opts;then
        #default parameters #arg required
        /usr/share/qa/tools/remote_qa_db_report.pl -b -m "${SQ_HOSTNAME}" -c "$comment" -T "${run_id}" 2>&1 | tee "/tmp/submission-$logname.log"
        if ! grep -iq "submission.php?submission_id=" "/tmp/submission-$logname.log";then
            echo "[qadb] $logname submit qa_db_report failed!" |tee -a "/root/failed.list"
	    cat "/tmp/submission-$logname.log" >>"/root/failed.detail"
        else
            echo "[qadb] $logname submit qa_db_report succeed!"
        fi
    else
        /usr/share/qa/tools/remote_qa_db_report.pl $remote_script_opts
        if ! grep -iq "submission.php?submission_id=" "/tmp/submission-$logname.log";then
            echo "[qadb] $logname submit qa_db_report failed!"|tee -a "/root/failed.list"
	    cat "/tmp/submission-$logname.log" >>"/root/failed.detail"
        else
            echo "[qadb] $logname submit qa_db_report succeed!"
        fi
    fi
    rm /tmp/submission-$logname.log
}

function switch_qadb () {
    if test "$databse"=="cn";then
       echo 'remote_qa_db_report_host="147.2.207.30"' >"/etc/qa/99-qa_tools-qaset"
       echo 'remote_qa_db_report_user="rd-qa"' >>"/etc/qa/99-qa_tools-qaset"  
    else
       echo 'remote_qa_db_report_host="qadb2.suse.de"' >"/etc/qa/99-qa_tools-qaset"
       echo 'remote_qa_db_report_user="qadb_report"' >>"/etc/qa/99-qa_tools-qaset"  
    fi  
    action=$1
    if test "$action"="clean";then
        rm "/etc/qa/99-qa_tools-qaset"
    fi        
}


#1 get log
switch_qadb

getconfig

if [ "$testsuite" = "a" ];then
    exit
    submitalllogs

else
    submitonelog "$testsuite"
fi

switch_qadb "clean"

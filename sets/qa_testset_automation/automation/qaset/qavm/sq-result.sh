#!/bin/bash
#
# QADB tools
#

function sq_qadb_load_comment {
    test -f ${SQ_QADB_COMMENT_FILE} && source ${SQ_QADB_COMMENT_FILE}
}

function sq_qadb_save_comment {
    echo "SQ_QADB_COMMENT='${SQ_QADB_COMMENT}'" > ${SQ_QADB_COMMENT_FILE}
}

function sq_qadb_set_comment {
    SQ_QADB_COMMENT="$1"
    sq_qadb_save_comment
}

function sq_qadb_reset_comment {
    SQ_QADB_COMMENT=
    sq_qadb_save_comment
}

function sq_qadb_is_empty_comment {
    test -z ${SQ_QADB_COMMENT}
}

function sq_qadb_load_run_id {
    test -f ${SQ_TEST_RUN_ID_FILE} && source ${SQ_TEST_RUN_ID_FILE}
}

function sq_qadb_save_run_id {
    echo "SQ_TEST_RUN_ID=${SQ_TEST_RUN_ID}" > ${SQ_TEST_RUN_ID_FILE}
}

function sq_qadb_set_run_id {
    SQ_TEST_RUN_ID=$1
    sq_qadb_save_run_id
}

function sq_qadb_is_empty_run_id {
    test -z ${SQ_TEST_RUN_ID}
}

function sq_qadb_gen_run_id {
    SQ_TEST_RUN_ID=$(date '+%Y%m%d')
    sq_qadb_save_run_id
}

function sq_result_save_locally {
    local name=$1
    local ret=0

    _serial=$(date '+%Y%m%dT%H%M%S')
    pushd /var/log/qa/ctcs2 > /dev/null
    if test $? -eq 0;then
        tar -c -j -f "${SQ_TEST_LOG_DIR}/${name}-${_serial}.tar.bz2" *
    fi
    if test $? -ne 0;then
        sq_error "[result] Failed to save ${name}-${_serial}"
        ret=1
    else
        sq_info "[result] Succeeded to save ${name}-${_serial}"
        ret=0
    fi
    popd > /dev/null
    return $ret
}

function sq_qadb_update_system_infomation {
    for name in $(ls /var/log/qa/ctcs2); do
        echo $name | egrep "^.*[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}$" &&
            ! [ -f /var/log/qa/ctcs2/${name}/messages.syslog ] &&
            cp /var/log/messages /var/log/qa/ctcs2/${name}/messages.syslog  &&
            chmod 644 /var/log/qa/ctcs2/${name}/messages.syslog
        zypper pt -i > /var/log/qa/ctcs2/${name}/installed-pattern.txt
        lspci -k > /var/log/qa/ctcs2/${name}/lspci-k.txt
        lsmod > /var/log/qa/ctcs2/${name}/lsmod.txt
        lscpu > /var/log/qa/ctcs2/${name}/lscup.txt
        mount | grep ^/dev > /var/log/qa/ctcs2/${name}/partition-mount.txt
        cat /proc/cmdline > /var/log/qa/ctcs2/${name}/cmdline.txt
        cat /proc/meminfo > /var/log/qa/ctcs2/${name}/meminfo.txt
        cat /proc/zoneinfo > /var/log/qa/ctcs2/${name}/zoneinfo.txt
        systemctl list-units > /var/log/qa/ctcs2/${name}/systemctl-list-units.txt
    done
}

function sq_qadb_update_system_shortinfo {
    #if [ -e "/var/log/messages" ];then
    for name in $(ls /var/log/qa/ctcs2); do
        echo $name | egrep "^.*[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}$" &&
            ! [ -f /var/log/qa/ctcs2/${name}/messages.shortlog ] &&
        awk 'BEGIN{ key["error"]=0;key["calltrace"]=0;}{for(i in key){if($0~i){key[i]++;values[i]=values[i]""FNR""$0"\n";}}}END{for (i in key){print i" have "key[i];} for (i in key){print values[i] }}' /var/log/messages >> /var/log/qa/ctcs2/${name}/messages.shortlog &&
       chmod 644 /var/log/qa/ctcs2/${name}/messages.shortlog
    done
}
function sq_qadb_server_resotre {
    rm "/etc/qa/99-qa_tools-"*
}

function sq_qadb_server_switch {
#/etc/qa/00-qa_tools-default indcate where the reporter
    local _Beijing_addr
    local _Nuremberg_addr
    local _qadb_server_addr
    local _qadb_reporter
    local _Beijing_reporter
    local _Nuremberg_reporter
    local _config_file
    local _sq_qadb2_server

    if echo ${SQ_TEST_RESULT_SERVER} | grep "Beijing" &>/dev/null ;then
        _sq_qadb2_server="Beijing"
    fi
    if ! [ -z ${1} ]; then
        _sq_qadb2_server=${1}
    fi

    _config_file="/etc/qa/99-qa_tools-apac2"

    #remove others
    rm "/etc/qa/99-qa_tools-"*
    #to be only one
    cp -v "/etc/qa/00-qa_tools-default" ${_config_file}

    _Beijing_addr="147.2.207.30"
    _Beijing_reporter="rd-qa"
    _Nuremberg_addr="qadb2.suse.de"
    _Nuremberg_reporter="qadb_report"

    if [ "${_sq_qadb2_server}x" = "Beijingx" ]; then
        _qadb_server_addr=${_Beijing_addr}
        _qadb_reporter=${_Beijing_reporter}
    else
        _qadb_server_addr=${_Nuremberg_addr}
        _qadb_reporter=${_Nuremberg_reporter}
    fi

    sed -i "s/^remote_qa_db_report_host=.*$/remote_qa_db_report_host=\"${_qadb_server_addr}\"/g" ${_config_file}
    sed -i "s/^remote_qa_db_report_user=.*$/remote_qa_db_report_user=\"${_qadb_reporter}\"/g" ${_config_file}
}

function sq_qadb_submit_result_for_run {
    local _sq_run
    local _serial
    local _db_echo
    local _comment
    local _result
    local _run_id

    _sq_run=$1
    #if grep bej\.suse\.com /etc/HOSTNAME > /dev/null
    # use the command instead of the variable. Because
    # hostname could be change by dhcp but HOSTNAME is inherited from the screen
    # which starts at the begining of the running host.
    if ip -4 addr | grep "inet 147\.2\." > /dev/null;then
        SQ_HOSTNAME=$(hostname).apac.novell.com
    else
        SQ_HOSTNAME=$(hostname)
    fi
    sq_info "[QADB] TODO submit result!!!"

    if test "X${SQ_DEBUG_ON}" == "XYES";then
        _db_echo=echo
    else
        _db_echo=""
    fi

    if sq_qadb_is_empty_run_id; then
        _run_id=ACAP2
    else
        _run_id="ACAP2-${SQ_TEST_RUN_ID}"
    fi
    sq_debug "[qadb] run_id is ${_run_id}"

    _result="${_sq_run}-${_run_id}"

    if sq_qadb_is_empty_comment; then
        _comment="${_sq_run}"
    else
        _comment="${_sq_run} ${SQ_QADB_COMMENT}"
        _result="${_result}-${SQ_QADB_COMMENT}"
    fi
    sq_debug "[qadb] comment is ${_comment}"

    sq_qadb_update_system_infomation

    sq_qadb_update_system_shortinfo

    sq_result_save_locally "${_result}"

    sq_qadb_server_switch Nuremberg
    ${_db_echo} /usr/share/qa/tools/remote_qa_db_report.pl -L -b -m "${SQ_HOSTNAME}" -c "$(uname -r)" 2>&1 | tee "/tmp/submission-${_sq_run}.log"
    sq_qadb_server_resotre
    cat "/tmp/submission-${_sq_run}.log" >>"${SQ_TEST_SUBMISSION_DIR}/submission-${_sq_run}.log"
    if ! grep -iq "submission.php?submission_id=" "/tmp/submission-${_sq_run}.log";then
        sq_warn "[qadb] ${_sq_run} submit qa_db_report Nuremberg failed!"
        echo "${_sq_run}-${_serial}-Nuremberg" >>${SQ_USER_CONFIG_SUBMIT_FAILURE}
    else
       sq_info "[qadb] ${_sq_run} submit qa_db_report Nuremberg succeed!"
    fi
    rm /tmp/submission-${_sq_run}.log ${SQ_TEST_LOG_DIR}/qadb-Nuremberg-submission-${_result}-${_serial}.log

#upload log to Beijing QADB2 server
    if [ "${SQ_UPLOAD_TO_BEIJING}x" == "Enabledx" ]; then
        sq_qadb_server_switch Beijing
        ${_db_echo} /usr/share/qa/tools/remote_qa_db_report.pl -L -b -m "${SQ_HOSTNAME}" -c "$(uname -r)" 2>&1 | tee "/tmp/submission-${_sq_run}.log"
        sq_qadb_server_resotre
        cat "/tmp/submission-${_sq_run}.log" >>"${SQ_TEST_SUBMISSION_DIR}/submission-Beijing-${_sq_run}.log"
        if ! grep -iq "submission.php?submission_id=" "/tmp/submission-${_sq_run}.log";then
            sq_warn "[qadb] ${_sq_run} submit qa_db_report Beijing failed!"
        echo "${_sq_run}-${_serial}-Beijing" >>${SQ_USER_CONFIG_SUBMIT_FAILURE}
        else
            sq_info "[qadb] ${_sq_run} submit qa_db_report Beijing succeed!"
        fi
    fi
    rm /tmp/submission-${_sq_run}.log ${SQ_TEST_LOG_DIR}/qadb-Beijing-submission-${_result}-${_serial}.log


    # the result has been already backed
    # clean for the next run.
    rm -rf /var/log/qa/ctcs2/*
}

function sq_result_one_run {
    local _run=$1
    local _status
    sq_qadb_submit_result_for_run ${_run}
}

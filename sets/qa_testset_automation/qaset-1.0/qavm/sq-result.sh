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

    sq_result_save_locally "${_result}"

    ${_db_echo} /usr/share/qa/tools/remote_qa_db_report.pl -b -m "${SQ_HOSTNAME}" -c "${_comment}" -T "${_run_id}"

    if test $? -ne 0;then
        sq_warn "[qadb] Submit qa_db_report failed!"
        # the result has been already backed
        # clean for the next run.
        rm -rf /var/log/qa/ctcs2/* 
    fi
}

function sq_result_one_run {
    local _run=$1
    local _status
    sq_qadb_submit_result_for_run ${_run}
}

#!/bin/bash
#
# Message tools
#

#@ SQ_MSG_FILE

if test "X${SQ_MSG_FILE}" != "X" && test -f ${SQ_MSG_FILE};then
    _LOG_FILE_P=YES
else
    _LOG_FILE_P=NO
fi

function log_file_p {
    test "X${_LOG_FILE_P}" == "XYES" && return 0
}

function sq_msg {
    local lv=$1
    shift
    local prefix
    local _p

    case ${lv} in
        Error*)
            prefix="\033[0;31mERROR\033[0m"
            _p=E
            ;;
        Info*)
            prefix="\033[0;33mINFO\033[0m"
            _p=I
            ;;
        Warn*)
            prefix="\033[0;35mWARN\033[0m"
            _p=W
            ;;
        Debug*)
            prefix="\033[0;32mDEBUG\033[0m"
            _p=D
            ;;
        *) # not a proper one
            prefix="\033[0;31m${lv}\033[0m"
            _p=O
            ;;
    esac

    echo -e "[SLE-QA] ${prefix}\t$1" >&2
    log_file_p && echo ${_p} >> ${SQ_MSG_FILE}
    (
        shift
        while test $# -gt 0; do
            echo -e "\t\t$1"
            log_file_p && echo "\t\t$1" >> ${SQ_MSG_FILE}
            shift
        done
    ) >&2
}

function sq_debug {
    if test "X${SQ_DEBUG_ON}" == "XYES"; then
        sq_msg Debug "$@"
    fi
}

function sq_info {
    sq_msg Info "$@"
}

function sq_warn {
    sq_msg Warn "$@"
}

function sq_error {
    sq_msg Error "$@"
}

function sq_assert {
    sq_msg Assert "$@"
    exit 4
}

function sq_network_dump {
    sq_info "[network] dump"
    ip a
    ip r
    cat /etc/resolv.conf
    echo
}

#
# Repo tools
#
function sq_prep_repos {
    local _arch=$1
    local _SLE_build=$2
    local _repo_mirror=$3

    local _repo_url
    local _repo_name
    local _repos_num

    _repos_num=${#SQ_REPO_NAMES[*]}
    if test $_repos_num -le 0;then
        sq_warn "There is NO repo to be added." \
            "Please check the conf file!"
        return 1  ## no repo to be added
    else
        sq_info "There are ${_repos_num} repos to be added."
    fi

    for _repo_name in ${SQ_REPO_NAMES[*]};do
        _repo_url=$(sq_prep_${SLE_RELEASE}_get_repo_url_by_name ${_repo_name} ${_SLE_build} ${_arch} ${_repo_mirror})
        sq_info "add and ref repo" \
            "${_repo_name}" \
            "${_repo_url}"
        #delete the old one
        ${SQ_DEBUG_ECHO} zypper rr ${_repo_name}
        ${SQ_DEBUG_ECHO} zypper --no-gpg-checks -n ar -f ${_repo_url} ${_repo_name}
        if [ $? != 0 ];then
            sq_error "zypper add repo ${_repo_name} failed." \
                "The URI is\n\t${_repo_url}"
            return 2 #return or exit ??
        fi
        ${SQ_DEBUG_ECHO} zypper --gpg-auto-import-keys -n ref ${_repo_name}
        if [ $? != 0 ];then
            sq_error "zypper refresh repo ${_repo_name} failed." \
                "Check the connection to server"
            return 3
        fi
    done
    return 0
}

function sq_prep_install_packages_qa_libs {
    if test ${#SQ_LIBS[*]} -le 0;then
        sq_error "The SQ_LIBS has no packages!" \
            "Please check the conf file"
        return 1
    fi
    ${SQ_DEBUG_ECHO} zypper -n in -l ${SQ_LIBS[*]}
    if [ $? != 0 ];then
        sq_error "install packages for qa_LIBS failed!"
        #ignore missed packages
        #return 2
    fi
    return 0
}

function sq_prep_install_package_nocheck {
    local try
    sq_info "Try to install ${1}"
    try=0;
    while test $try -lt 10;do
        sq_network_dump
        zypper -n in -l ${1} && break
        sq_info "Try to install $try times"
        sq_info "Wait 10 secs"
        sleep 10
        let try++
    done
    if [ $? != 0 ];then
        sq_error "Failed to install ${1}\n"
        return 2
    fi
    return 0
}

function sq_prep_install_package {
    local pkg=$1
#    if rpm -q $pkg > /dev/null; then
#        sq_info "[package] $pkg already installed"
#        return 0
#    else
    sq_prep_install_package_nocheck $pkg
#    fi
}

function sq_prep_repos_and_packages {
    local _arch=$1
    local _SLE_build=$2
    local _repo_mirror=$3

    sq_prep_repos ${_arch} ${_SLE_build} ${_repo_mirror} && \
        sq_prep_install_packages_qa_libs

    if test $? -ne 0;then
        exit 5
        rm -f ${_autorun_lock}
    fi
}

#
# OS tools
#
function sq_os_get_sysinfo {
    # get the release
    SLE_BUILD=`egrep -o '([aA]lpha|[bB]eta|RC)[1-9]' /etc/issue`
    if [ -z "${SLE_BUILD}" ]; then
        SLE_BUILD="GMC"
        #TODO to get the meanings of GM and GMC
    fi

    ARCH=$HOSTTYPE
    if [ "$ARCH" != "" ]; then
        case $ARCH in
            i[3-9]86)  ARCH="i586";;
            p*pc) ARCH="ppc";;
            p*pc64) ARCH="ppc64";;
            # TODO ppc64le
        esac
    else
        sq_error "cannot determine architecture";
        exit 3
    fi

    REPO_MIRROR="DE"
    sq_info "[GLOBAL] ARCH: ${ARCH}" \
        "[GLOBAL] SLE_BUILD: ${SLE_BUILD}" \
        "[GLOBAL] REPO_MIRROR: ${REPO_MIRROR}"
}

function sq_os_reboot_2 {
    wall "REBOOT by qaset!!!"
    sleep 3
    /sbin/reboot
}

function sq_os_reboot {
    wall "REBOOT by sqset!!!!!!"
    # TODO why env
    env /usr/bin/systemctl -f reboot
}

function remove_serice_bysystemctl {
   systemctl disable qaperf.service
   if [ $? != 0 ];then
       sq_error "disable service by systemctl failed."
   fi
}

function remove_service_byinitd {
    level=$(runlevel | awk '{print $2}')
    run_dir="/etc/init.d/rc${level}.d"
    if test -d ${run_dir}; then
        rm -rf ${run_dir}/S99qaset
    else #runlevel unknown
        rm -rf /etc/init.d/after.local
    fi
    if [ $? != 0 ];then
       sq_error "disable service by remove soft link failed."
    fi
}

# collect acceptance results and send mail
function get_test_results_file_list(){
    local _testsuit_name=${1}
    local _test_results_dir_list=`find ${SQ_CTCS2_OLDLOG_DIR} -type d -name *${_testsuit_name}*`
    if test "X${_test_results_dir_list}" != "X"; then
        for path in ${_test_results_dir_list}; do
            if test -f "${path}/${SQ_CTCS2_TEST_DONE_FILENAME}" ; then
                echo "${path}/${SQ_CTCS2_TEST_RESULTS_FILENAME} "
            fi
        done
    else
        return 1
    fi
}

function get_qadb_submission_url(){
    local _testsuit_name=${1}
    local _submission_log=${SQ_TEST_SUBMISSION_DIR}/submission-${_testsuit_name}.log
    if test -f ${_submission_log}; then
        echo "The submission url as below:"
        for line in $(grep submission_id ${_submission_log} | cut -d ' ' -f 5); do
            echo "http://${line##*http://}"
        done
    else
        echo "Not found submission log file."
        return 1
    fi
}

function analyze_test_results(){
    local _testsuit_name=${1}
    local _return="PASSED"
    local _skipped=""
    local _results_file_list=$(get_test_results_file_list ${_testsuit_name})
    if test "X${_results_file_list}" = "X"; then
        echo; echo "Not found test_results file."    
    else
        for result_file in ${_results_file_list}; do
            if `grep '^1 0' ${result_file} 2>&1 > /dev/null`; then
                _return="FAILED"
            fi
            if `grep '^0 0' ${result_file} 2>&1 > /dev/null`; then
                _skipped="with some skipped cases"
            fi
        done
        echo "${_return} ${_skipped}"
    fi
}

function get_test_results_and_submission_url(){
    local _testsuit_name=${1}
    echo; echo -n "The ${_testsuit_name} test result is: "
    analyze_test_results ${_testsuit_name}
    get_qadb_submission_url ${_testsuit_name}
}


function get_process_stress_results(){
    local _testsuit_name="process_stress"
    get_test_results_and_submission_url ${_testsuit_name}
    echo "PS: You can ignore the VMSTAT testcase in the process_stress test."
}

function get_fs_stress_results(){
    local _testsuit_name="fs_stress"
    get_test_results_and_submission_url ${_testsuit_name}
}

function get_sched_stress_results(){
    local _testsuit_name="sched_stress"
    get_test_results_and_submission_url ${_testsuit_name}
}

function get_acceptance_results(){
    get_process_stress_results
    get_fs_stress_results
    get_sched_stress_results
}

function send_mail(){
    local _title=${1}
    local _mail_address=${2}
    local _mail_text=${3}
    echo "${_mail_text}" | mail -s "${_title}" "${_mail_address}"
}

function send_mail_acceptance_test_results(){
    send_mail "${SQ_MAIL_TITLE_ACCEPTANCE}" "${SQ_MAIL_ADDRESS_ACCEPTANCE}" "$(get_acceptance_results)"
}

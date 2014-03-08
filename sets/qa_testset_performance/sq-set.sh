#!/bin/bash

if test $UID -ne 0;then
    sq_error "I need root permission!!!"
    exit 1
fi

SQ_TEST_INVOKE_DIR=$(pwd)
SQ_TEST_INVOKE_NAME=$0

CMDPATH=$(which $0)
if [ -L $CMDPATH ];then
    pushd $(dirname $CMDPATH) > /dev/null
    CMDTARGET=$(readlink $CMDPATH)
    pushd $(dirname $CMDTARGET) > /dev/null
    readonly __IMPORT_ROOT=$(pwd)
    popd > /dev/null
    popd > /dev/null
else
    pushd $(dirname $CMDPATH) > /dev/null
    readonly __IMPORT_ROOT=$(pwd)
    popd > /dev/null
fi

function __import {
    # TODO check $1 is *.sh
    # NOTE absolute path is not supported.
    local _lock
    if test "X${__IMPORT_ROOT}" == "X";then
        echo "[IMPORT] ERROR __IMPORT_ROOT is NULL"
        exit 1
    fi
    _lock=$(echo $1 | tr '[a-z./\-]' '[A-Z___]')
    if eval "test X\$${_lock}_IMPORTED != XYES";then
        source ${__IMPORT_ROOT}/$1
        eval "readonly ${_lock}_IMPORTED=YES"
    else
        : echo "[IMPORT] $1 has already been imported!"
    fi
}

__import sq-mach.sh
__import sq-global.sh
__import sq-util.sh

if test $# -lt 1;then
    usage
fi

if test "X${SQ_SET_CALL_BY_WRAP}" == "XYES";then
    SQ_SET_ARGV="$@"
fi

sq_global_init
sq_info "[GLOBAL] Start at $(date)"
sq_info "[GLOBAL] /proc/uptime: $(cat /proc/uptime)"

# program initialization
function usage {
    echo "Usage $0 subcmd options"
    exit 1
}

sq_os_get_sysinfo

function sq_set_cmd_run_parse {
    local _opt
    while test $# -gt 0;do
        _opt=$1
        shift
        case $_opt in
            '-t') #target SLE_RELEASE
                if test $# -gt 0;then
                    SLE_RELEASE=$1
                    shift
                else
                    usage
                fi
                ;;
            '-l')
                if test $# -gt 0;then
                    SQ_TEST_RUN_LIST_FILE=$1
                    shift
                else
                    usage
                fi
                ;;
            '-s')
                if test $# -gt 0;then
                    SQ_TEST_RUN_SET_FILE=$1
                    shift
                else
                    usage
                fi
                ;;
             *)
                usage;;
        esac
    done
    if test "X${SLE_RELEASE}" == "X" && \
        test "X${SQ_TEST_RUN_LIST_FILE}" == "X" && \
        test "X{SQ_TEST_RUN_SET_FILE}" == "X"
        then
        usage
    fi
}

function sq_set_cmd_run_list {
    if test "X${SQ_SET_CALL_BY_WRAP}" == "XYES";then
        export SQ_SET_CALL_BY_WRAP=NO
        cd ${SQ_TEST_CALL_DIR}
        echo 'logfile %t.%Y-%m-%d.%c.%H.screenlog' > screenrc
        exec screen -L -S ${SQ_TEST_RUN_LIST_FILE}-${SQ_TEST_RUN_SET_FILE} \
            -t ${SQ_TEST_RUN_LIST_FILE}-${SQ_TEST_RUN_SET_FILE} -c screenrc -d -m \
            ${SQ_TEST_INVOKE_NAME} ${SQ_SET_ARGV}

    else
        sq_mach_run
    fi
}

function sq_set_cmd_reset {
    rm -f ${SQ_TEST_CONTROL_FILE_STOP} 1> /dev/null 2>&1
    rm -f ${SQ_TEST_CONTROL_FILE_DONE} 1> /dev/null 2>&1
    rm -f ${SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY} 1> /dev/null 2>&1
    echo > ${SQ_TEST_CONTROL_FILE_NEXT_RUN}
}

function sq_set_cmd_prepo_parse {
    local _opt
    while test $# -gt 0;do
        _opt=$1
        shift
        case $_opt in
            '-t') #target SLE_RELEASE
                if test $# -gt 0;then
                    SLE_RELEASE=$1
                    shift
                else
                    usage
                fi
                ;;
            *)
                usage;;
        esac
    done
    if test "X${SLE_RELEASE}" == "X";then
        usage
    fi
}

function sq_set_cmd_prepo {
    sq_info "[PREPO] Preparation: is doing"
    sq_prep_repos_and_packages ${ARCH} ${SLE_BUILD} ${REPO_MIRROR}
    if test $? -ne 0;then
        sq_error "[PREPO] preparation: failed!"
        return 1
    fi
    echo "$(date)" > ${SQ_TEST_CONTROL_FILE_PREPARED}
}

function sq_set_cmd_stop_list {
    echo > ${SQ_TEST_CONTROL_FILE_STOP}
}

function sq_set_cmd_resume_list {    
    rm -f ${SQ_TEST_CONTROL_FILE_STOP} 1> /dev/null 2>&1
    sq_warn "RESUME not finished!!!" \
        "Only delete STOP file" \
        "You need manually run the list again!!!"
}

case $1 in
    run*) shift; sq_set_cmd_run_parse "$@"
        sq_set_cmd_run_list
        ;;
    reset*) shift; sq_set_cmd_reset
        ;;
    prepo*)
        shift; sq_set_cmd_prepo_parse "$@"
        sq_set_cmd_prepo
        ;;
    stop*)
        shift; sq_set_cmd_stop_list
        ;;
    resume*)
        shift; sq_set_cmd_resume_list
        ;;
    *) usage
        ;;
esac

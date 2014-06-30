#!/bin/bash

### setup an import mechanism
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

__import sq-global.sh
__import sq-util.sh
__import sq-execute.sh

#
# the control of all executions
# =============================
#
function sq_control_open {
    sq_debug "[CONTROL] Preparation: tag system clean."
    rm -f ${SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY} 2>/dev/null

    #TODO make this option cmdlined
    SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=NO
    SQ_TEST_CONTROL_MAKE_SYSTEM_PURE=NO

    if test "X${SQ_TEST_CONTROL_PARALELL}" == "XYES";then
        SQ_TEST_CONTROL_PARALELL_NOWAIT=nowait
    else
        SQ_TEST_CONTROL_PARALELL_NOWAIT=""
    fi
    # import the run cases
    __import ${SQ_TEST_RUN_SET_FILE}.set
    # TODO make the list as a absolute path
    # SQ_TEST_INVOKE_DIR
    if test ${#SQ_TEST_RUN_LIST[@]} -gt 0;then
        sq_info "[CONTROL] use customized run list"
    else
        sq_info "[CONTROL] use default run list from ${SQ_TEST_RUN_LIST_FILE}"
        __import ${SQ_TEST_RUN_LIST_FILE}.list
    fi
}

function sq_control_close {
    if test -f ${SQ_TEST_CONTROL_FILE_STOP};then
        sq_info "[CONTROL]: runs stopped"
        return
    fi
    if test -f ${SQ_TEST_CONTROL_FILE_DONE};then
        sq_info "[CONTROL]: runs done. NO reboot"
        return
    fi
    if test "X${SQ_TEST_CONTROL_MAKE_SYSTEM_PURE}" == "XYES";then
        SQ_TEST_MACH_FLAG_REBOOT=YES
        sq_info "[CONTROL]: NEED to reboot system."
    fi
}

function sq_control_get_next_run {
    ### the control policy

    if test -f ${SQ_TEST_CONTROL_FILE_STOP};then
        sq_info "[CONTROL]: this run is manually stopped!"
        return 1
    fi

    if test -f ${SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY};then
        SQ_TEST_CONTROL_MAKE_SYSTEM_PURE=YES
        sq_debug "[CONTROL]: This system is dirty."
        if test "X${SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY}" == "XNO";then
            return 2
        fi
    fi

    if test -f ${SQ_TEST_CONTROL_FILE_DONE};then
        sq_info "[CONTROL]: This round of runs was already finished at $(cat ${SQ_TEST_CONTROL_FILE_DONE})"
        return 3
    fi

    ### the operation of run lists
    if test ${#SQ_TEST_RUN_LIST[*]} -le 0;then
        sq_error "SQ_TEST_RUN_LIST is none" \
            "Plase check the ${SLE_RELEASE}.list file."
         return 4
    fi

    sq_debug "[CONTROL] TRY A NEW RUN ##################"
    if test -f ${SQ_TEST_CONTROL_FILE_NEXT_RUN};then
        read SQ_THIS_RUN_INDEX SQ_THIS_RUN < ${SQ_TEST_CONTROL_FILE_NEXT_RUN}
    else
        SQ_THIS_RUN_INDEX=""
        SQ_THIS_RUN=""
    fi

    if test "X${SQ_THIS_RUN_INDEX}" == "X";then
        SQ_THIS_RUN_INDEX=0
    fi

    if test $SQ_THIS_RUN_INDEX -ge ${#SQ_TEST_RUN_LIST[*]};then
        sq_error "the run list is out of SQ_TEST_RUN_LIST"
        #TODO check this exit 
        exit -1
    fi

    SQ_THIS_RUN="${SQ_TEST_RUN_LIST[$SQ_THIS_RUN_INDEX]}"
    sq_debug "[CONTROL] THIS RUN: ${SQ_THIS_RUN}"
    sq_debug "[CONTROL] THIS RUN INDEX ${SQ_THIS_RUN_INDEX}"

    SQ_NEXT_RUN_INDEX=$(($SQ_THIS_RUN_INDEX + 1))
    if test $SQ_NEXT_RUN_INDEX -ge ${#SQ_TEST_RUN_LIST[*]};then
        echo > ${SQ_TEST_CONTROL_FILE_NEXT_RUN}
        sq_debug "[CONTROL] THIS RUN is the last one."        
        SQ_NEXT_RUN_INDEX=""
        SQ_NEXT_RUN=""
    else
        SQ_NEXT_RUN="${SQ_TEST_RUN_LIST[$SQ_NEXT_RUN_INDEX]}"
        sq_debug "[CONTROL] NEXT RUN: ${SQ_NEXT_RUN}"
    fi

    echo "${SQ_NEXT_RUN_INDEX}" "${SQ_NEXT_RUN}" > ${SQ_TEST_CONTROL_FILE_NEXT_RUN}
}

function sq_control_get_run_status {
    local _run_ret

    _run_ret=$1

    if test ${_run_ret} -eq 0;then
        sq_debug "[CONTROL]: tag the system dirty"
        echo "$(date '+%Y-%m-%d-%H-%M-%S')" > ${SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY}
    else
        true
        # TODO save a list of all the failed runs
        # TODO more
    fi
}

function sq_control_check_run_queue {
    if test $(($SQ_THIS_RUN_INDEX + 1)) -ge ${#SQ_TEST_RUN_LIST[*]};then
        echo "$(date '+%Y-%m-%d-%H-%M-%S')" > ${SQ_TEST_CONTROL_FILE_DONE}
    fi
}

function sq_control_special_form_reboot_off {
    #_continue
    SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=YES
    sq_info "[CONTROL] reboot is disable"
}

function sq_control_special_form_reboot_on {
    SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=NO
    sq_info "[CONTROL] reboot is enable"
}

function sq_control_run {
    sq_control_open ${ARCH} ${SLE_BUILD} ${REPO_MIRROR}
    while sq_control_get_next_run;do
        # _* special form
        case ${SQ_THIS_RUN} in
            _reboot_off)
                sq_control_special_form_reboot_off
                ;;
            _reboot_on)
                sq_control_special_form_reboot_on
                ;;
            _*)
                sq_debug '[CONTROL] Unknown special form ${SQ_THIS_RUN}'
                ;;
            *)
                sq_execute_run ${SQ_THIS_RUN} ${SQ_CONTROL_PARALELL_NOWAIT}
                sq_control_get_run_status $?
                ;;
        esac
        sq_control_check_run_queue
    done
    sq_control_close
}

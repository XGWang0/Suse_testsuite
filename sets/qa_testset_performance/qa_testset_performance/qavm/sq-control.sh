#!/bin/bash

__import qavm/sq-global.sh
__import qavm/sq-util.sh
__import qavm/sq-execute.sh

#
# the control of all executions
# =============================
#
function sq_control_open {
    sq_debug "[CONTROL] Preparation: tag system clean."
    rm -f ${SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY} 2>/dev/null

    if test "X${SQ_TEST_CONTROL_PARALELL}" == "XYES";then
        SQ_TEST_CONTROL_PARALELL_NOWAIT=nowait
        SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=YES
    else
        SQ_TEST_CONTROL_PARALELL_NOWAIT=""
        SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=NO
    fi

    SQ_TEST_CONTROL_MAKE_SYSTEM_PURE=NO

    # import the run cases
    if test -z ${SQ_TEST_RUN_SET}; then
        sq_error "No test set"
        sq_error "Check the configure file!!"
        return 5
    fi
    __import set/${SQ_TEST_RUN_SET}.set
    if test $? -ne 0;then
        sq_error "set dose NOT exist"
        return 5
    fi

    __import ${SQ_USER_CONFIG_LIST}
    if test ${#SQ_TEST_RUN_LIST[@]} -gt 0;then
        sq_info "[CONTROL] use customized run list"
    else
        sq_info "[CONTROL] use default run list for ${SQ_TEST_RUN_SET}"
        if test ${SQ_TEST_RUN_SET} == fake;then
            __import list/${SQ_TEST_RUN_SET}.list
        else
            __import list/${SQ_TEST_RUN_SET}-${SLE_RELEASE}.list
        fi
    fi
    if debugp; then
        sq_info "[CONTROL] run list:"
        for name in ${SQ_TEST_RUN_LIST[@]};do
            sq_info "[CONTROL]    ${name}"
        done
    fi
    sq_qadb_load_comment
    return 0
}

function sq_control_close {

    if test "X${SQ_TEST_CONTROL_PARALELL}" == "XYES";then
        jobs -p
        sq_info "[CONTROL] TODO submit the log for PARALELL running"
        wait
    fi

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
            "Plase check the list file."
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
    if test "X${SQ_TEST_CONTROL_PARALELL}" == "XYES";then
        sq_info "[CONTROL] It is meaningless to enable reboot with PARALELL"
        return
    fi
    SQ_TEST_CONTROL_IGNORE_SYSTEM_DIRTY=NO
    sq_info "[CONTROL] reboot is enable"
}

function eval_result_comment {
    local _comment
    if test $(type -t $1) == "function";then
        comment=$(eval $1)
        sq_qadb_set_comment "${comment}"
    else
        sq_warn "[CONTROL] unknown comment function"
    fi
}

function sq_control_run {
    sq_control_open ${ARCH} ${SLE_BUILD} ${REPO_MIRROR}
    if test $? -ne 0; then
        return 5
    fi
    while sq_control_get_next_run;do
        # _* special form
        # TODO better name
        case ${SQ_THIS_RUN} in
            _reboot_off)
                sq_control_special_form_reboot_off
                ;;
            _reboot_on)
                sq_control_special_form_reboot_on
                ;;
            _result_comment*)
                eval_result_comment ${SQ_THIS_RUN}
                ;;
            _*)
                sq_debug '[CONTROL] Unknown special form ${SQ_THIS_RUN}'
                ;;
            *)
                sq_execute_run ${SQ_THIS_RUN} ${SQ_TEST_CONTROL_PARALELL_NOWAIT}
                sq_control_get_run_status $?
                ;;
        esac
        sq_control_check_run_queue
    done
    sq_control_close
}

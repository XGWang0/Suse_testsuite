#!/bin/bash

__import qavm/sq-global.sh
__import qavm/sq-util.sh
__import qavm/sq-result.sh
__import qavm/sq-hook.sh

SQ_EXE_DEBUG_SCRIPT=${__IMPORT_ROOT}/qavm/sq-fake.sh

function sq_execute_init {
    sq_hook_list_new EXE_CLOSE
}
#
# the execution of a run
# ----------------------
function sq_execute_open {
    local _n=${SQ_EXE_RUN_NAME}
    local _p
    local _l
    local _i

    sq_info "[EXE] ${_n}: starting ..."
    _i=0
    eval "_l=\${#${_n}_packages[@]}"
    sq_debug "[EXE] #packages for ${_n} is ${_l}"
    while test ${_i} -lt ${_l};do
        eval "_p=\${${_n}_packages[$_i]}"
        sq_debug "[EXE] try to install package ${_p}"
        sq_prep_install_package ${_p} || return $?
        let _i++
    done

    if test "X$(type -t ${_n}_open)" == "Xfunction";then
        sq_debug "[EXE] ${_n}: ${_n}_open ing..."
        ${_n}_open ${ARCH} ${SLE_BUILD}
    else
        sq_debug "[EXE] ${_n}: opening..."
        true
    fi
}

function sq_execute_check_script {
    local _n=${SQ_EXE_RUN_NAME}
    local _s

    if eval "test \"X\${${_n}_run}\" == X";then
        _s="/usr/share/qa/tools/test_${_n}-run"
        sq_debug "[EXE] ${_n}: [G] ${_s}"
    else
        eval "_s=\${${_n}_run}"
        sq_debug "[EXE] ${_n}: [S] ${_s}"
    fi

    if test ! -x ${_s};then
        sq_error "[EXE] ${_n}: ${_s} dose not exist!!!"
        return 1
    else
        if test $SQ_DEBUG_ON == YES;then
            SQ_EXE_RUN_SCRIPT=${SQ_EXE_DEBUG_SCRIPT}
        else
            SQ_EXE_RUN_SCRIPT=${_s}
        fi
        return 0
    fi
}

function sq_execute_close {
    local _n=${SQ_EXE_RUN_NAME}
    if test "X$(type -t ${_n}_close)" == "Xfunction";then
        sq_debug "[EXE] ${_n}: ${_n}_close ing..."
        ${_n}_close ${ARCH} ${SLE_BUILD}
    else
        sq_debug "[EXE] ${_n}: closing"
    fi
    sq_execute_submit_log
    sq_hook_list_foreach EXE_CLOSE
}

function sq_execute_submit_log {
    if test "X${SQ_EXE_RUN_NOWAIT}" == "XYES";then
        sq_info "[EXE] ignore the submition of qadb log"
        sq_info "[EXE] please submit the log manully"
    else
        sq_result_one_run ${SQ_EXE_RUN_NAME} ${SQ_EXECUTE_END_STATUS}
    fi
}

function sq_execute_succeeded {
    SQ_EXECUTE_END_STATUS=SUCCEEDED
    sq_execute_close
}

function sq_execute_failed {
    SQ_EXECUTE_END_STATUS=FAILED
    sq_execute_close
}

function sq_execute_call {
    local _n=${SQ_EXE_RUN_NAME}
    local _s=${SQ_EXE_RUN_SCRIPT}
    local _o
    local screenrc
    local dsuf

    pushd ${SQ_TEST_RUN_DIR} > /dev/null
    #TODO a better place for screenlog
    dsuf=$(date +%m%dT%H%M)
    screenrc=${_n}.screenrc
    echo "logfile ${_n}-${dsuf}.screenlog" > ${screenrc}
    # TODO backgroud call
    # TODO paralell call
    if test "X${SQ_EXE_RUN_NOWAIT}" == "XYES";then
        _o='-d'
    else
        _o='-D'
    fi
    # save info into /var/log/message for debuging within the whole system context.
    logger "[QA_SET] starting ${SQ_EXE_RUN_NAME}"
    if test "X$(type -t ${_n}_get_args)" == "Xfunction";then
        sq_debug "[EXE] ${_n}: ${_n}_get_args ing..."
        sq_info "[EXE] ${_n}: running"
        screen -L -S ${_n} -t ${_n} -c ${screenrc} ${_o} -m "${_s}" $(${_n}_get_args)
    else
        sq_info "[EXE] ${_n}: running"
        screen -L -S ${_n} -t ${_n} -c ${screenrc} ${_o} -m "${_s}"
    fi

    if test "X${SQ_EXE_RUN_NOWAIT}" == "XYES";then
        logger "[QA_SET] started ${SQ_EXE_RUN_NAME}"
        sq_info "[EXE] ${_n}: started"
    else
        logger "[QA_SET] finished ${SQ_EXE_RUN_NAME}"
        sq_info "[EXE] ${_n}: finished"
    fi

    popd > /dev/null
}

function sq_execute_run {
    local _run_name
    local _exe_stage
    local _result
    local _nowait

    _run_name=$1
    _nowait=$2
    _exe_stage=EXE_STAGE_START

    if test "X${_nowait}" == "Xnowait";then
        SQ_EXE_RUN_NOWAIT=YES
    fi

    while true;do
        if test "X${_exe_stage}" == "XEXE_STAGE_END";then
            break
        fi
        case ${_exe_stage} in
            EXE_STAGE_START)
                SQ_EXE_RUN_NAME=${_run_name}
                SQ_EXE_RUN_SCRIPT=""
                _exe_stage=EXE_STAGE_OPEN
                ;;
            EXE_STAGE_OPEN)
                sq_execute_open
                if test $? -eq 0;then
                    _exe_stage=EXE_STAGE_CHECK_SCRIPT
                else
                    _result=EXE_RET_ERROR_OPEN
                    _exe_stage=EXE_STAGE_FAILED
                fi
                ;;
            EXE_STAGE_CHECK_SCRIPT)
                sq_execute_check_script
                if test $? -eq 0;then
                    _exe_stage=EXE_STAGE_CALL
                else
                    _result=EXE_RET_ERROR_SCRIPT
                    _exe_stage=EXE_STAGE_FAILED
                fi
                ;;
            EXE_STAGE_CALL)
                sq_execute_call
                if test $? -eq 0;then
                    _result=EXE_RET_OK_CALL
                    _exe_stage=EXE_STAGE_SUCCEEDED
                else
                    _result=EXE_RET_ERROR_CALL
                    _exe_stage=EXE_STAGE_FAILED
                fi
                ;;
            EXE_STAGE_SUCCEEDED)
                sq_execute_succeeded
                _exe_stage=EXE_STAGE_END
                ;;
            EXE_STAGE_FAILED)
                sq_execute_failed
                _exe_stage=EXE_STAGE_END
                ;;
            EXE_STAGE_END)
                : #nothing to do
                ;;
            *)
                sq_error "[EXE] NEVER be Here. BUGON"
                exit 9
                ;;
        esac
    done

    if test "x${_result}" == "xEXE_RET_OK_CALL";then
        return 0
    else
        return 1
    fi
}

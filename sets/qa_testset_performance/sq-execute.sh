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

SQ_EXE_DEBUG_SCRIPT=${__IMPORT_ROOT}/sq-fake.sh

#
# the execution of a run
# ----------------------
function sq_execute_open {
    local _n=${SQ_EXE_RUN_NAME}

    sq_info "[EXE] ${_n}: starting ..."
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
}

function sq_execute_close_and_submit_log {
    sq_execute_close
    sq_qadb_submit_result ${SQ_EXE_RUN_NAME}
}

function sq_execute_failed {
    sq_execute_close
    # TODO record the SQ_EXE_RUN_NAME
}

function sq_execute_call {
    local _n=${SQ_EXE_RUN_NAME}
    local _s=${SQ_EXE_RUN_SCRIPT}
    local _o

    pushd ${SQ_TEST_RUN_DIR} > /dev/null
    #TODO a better place for screenlog
    echo 'logfile %t.%Y-%m-%d.%c.%H.screenlog' > screenrc
    # TODO backgroud call
    # TODO paralell call
    if test "X${SQ_EXE_RUN_NOWAIT}" == "XYES";then
        _o='-d'
    else
        _o='-D'
    fi
    if test "X$(type -t ${_n}_get_args)" == "Xfunction";then
        sq_debug "[EXE] ${_n}: ${_n}_get_args ing..."
        sq_info "[EXE] ${_n}: running"
        screen -L -S ${_n} -t ${_n} -c screenrc ${_o} -m "${_s}" $(${_n}_get_args)
    else
        sq_info "[EXE] ${_n}: running"
        screen -L -S ${_n} -t ${_n} -c screenrc ${_o} -m "${_s}"
    fi
    sq_info "[EXE] ${_n}: finished"
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
                    _exe_stage=EXE_STAGE_CLOSE
                else
                    _result=EXE_RET_ERROR_CALL
                    _exe_stage=EXE_STAGE_CLOSE
                fi
                ;;
            EXE_STAGE_CLOSE)
                sq_execute_close_and_submit_log
                _exe_stage=EXE_STAGE_END
                ;;
            EXE_STAGE_FAILED)
                sq_execute_close
                _exe_stage=EXE_STAGE_END
                ;;
            EXE_STAGE_END)
                : #nothing to do
                ;;
            *)
                sq_error "[EXE] NEVER be Here. BUGON"
                ;;
        esac
    done

    if test "x${_result}" == "xEXE_RET_OK_CALL";then
        return 0
    else
        return 1
    fi
}

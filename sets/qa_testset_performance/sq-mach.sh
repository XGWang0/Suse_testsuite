#!/bin/bash
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

__import sq-control.sh
__import sq-global.sh
__import sq-util.sh

function sq_mach_open {
    if test -f ${SQ_TEST_CONTROL_FILE_PREPARED};then
        sq_info "[MACH] Preparation: NOT NEED."
    else
        sq_info "[MACH] Preparation: is doing"
        sq_prep_repos_and_packages ${ARCH} ${SLE_BUILD} ${REPO_MIRROR}
        if test $? -ne 0;then
            sq_error "[MACH] preparation: failed!"
            return 1
        fi
        echo "$(date)" > ${SQ_TEST_CONTROL_FILE_PREPARED}
    fi
    SQ_TEST_MACH_FLAG_REBOOT=NO
}


function sq_mach_close {
    if test "X${SQ_TEST_MACH_FLAG_REBOOT}" == "XYES";then
        case ${SLE_RELEASE} in
            SLE11SP3) sq_info "[MACH] Do not reboot in SLE11SP3"
                ;;
            SLE12) sq_os_reboot
                ;;
            *) sq_info "[MACH] Not implement rebooting in ${SLE_RELEASE}"
                ;;
        esac
    fi
}

function sq_mach_run {
    if sq_mach_open;then
        sq_control_run
    fi
    sq_mach_close
}

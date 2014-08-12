SQ_DEBUG_ON=NO

if test "X${SQ_DEBUG_ON}" == "XYES";then
    SQ_TEST_DIR=/var/log/qaset/debug
else
    SQ_TEST_DIR=/var/log/qaset
fi

SQ_TEST_RUN_DIR=${SQ_TEST_DIR}/runs
SQ_TEST_CALL_DIR=${SQ_TEST_DIR}/calls
SQ_TEST_CONTROL_DIR=${SQ_TEST_DIR}/control
SQ_TEST_LOG_DIR=${SQ_TEST_DIR}/log

SQ_TEST_CONTROL_FILE_PREPARED=${SQ_TEST_CONTROL_DIR}/PREPARED
SQ_TEST_CONTROL_FILE_STOP=${SQ_TEST_CONTROL_DIR}/STOP
SQ_TEST_CONTROL_FILE_DONE=${SQ_TEST_CONTROL_DIR}/DONE
SQ_TEST_CONTROL_FILE_NEXT_RUN=${SQ_TEST_CONTROL_DIR}/NEXT_RUN
SQ_TEST_CONTROL_FILE_SYSTEM_DIRTY=${SQ_TEST_CONTROL_DIR}/SYSTEM_DIRTY

SQ_TEST_CONTROL_PARALELL=NO

#default run list
SQ_TEST_RUN_LIST=()
SQ_TEST_RUN_LIST_FILE=""
SQ_TEST_RUN_SET_FILE=""
SQ_TEST_INVOKE_DIR=""
#ARCH
#SLE_BUILD
#REPO_MIRROR
#SLE_RELEASE

SQ_TEST_MACH_FLAG_REBOOT=NO

# user configuration
SQ_USER_CONFIG_DIR=/root/qaset
SQ_USER_CONFIG_FILE=${SQ_USER_CONFIG_DIR}/config

# qadb
SQ_TEST_QADB_COMMENT_TEMPLATE="%s"


function sq_global_init {
    if test ! -d ${SQ_TEST_DIR};then
        mkdir -p ${SQ_TEST_DIR}
        mkdir -p ${SQ_TEST_RUN_DIR}
        mkdir -p ${SQ_TEST_CALL_DIR}
        mkdir -p ${SQ_TEST_CONTROL_DIR}
        mkdir -p ${SQ_TEST_LOG_DIR}
    fi
    if test ! -d ${SQ_USER_CONFIG_DIR};then
        mkdir -p ${SQ_USER_CONFIG_DIR}
        touch ${SQ_USER_CONFIG_FILE}
    fi
}

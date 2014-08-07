function kgr_in_progress() {
    [ "$(cat /sys/kernel/kgraft/in_progress)" -ne 0 ]
}

function kgr_wait_complete() {
    if [ $# -gt 0 ]; then
        TIMEOUT=$1
    else
        TIMEOUT=-1
    fi

    while kgr_in_progress && [ $TIMEOUT -ne 0 ]; do
        sleep 1
        (( TIMEOUT-- )) || true
    done

    ! kgr_in_progress
}

function kgr_kick_processes() {
    for PROC in /proc/[0-9]*; do
        if [ "$(cat $PROC/kgr_in_progress)" -ne 0 ]; then
            PID=$(echo $PROC | cut -d/ -f3)
            kill -STOP $PID
            kill -CONT $PID
        fi
    done
}

declare -a RECOVERY_HOOKS

function push_recovery_fn() {
    [ -z "$1" ] && echo "WARNING: no parameters passed to push_recovery_fn"
    RECOVERY_HOOKS[${#RECOVERY_HOOKS[*]}]="$1"
}

function pop_and_run_recovery_fn() {
    local fn=$1
    local num_hook=${#RECOVERY_HOOKS[*]}

    [ $num_hook -eq 0 ] && return 1
    (( num_hook--)) || true
    eval ${RECOVERY_HOOKS[$num_hook]} || true
    unset RECOVERY_HOOKS[$num_hook]
    return 0
}

function call_recovery_hooks() {
    for fn in "${RECOVERY_HOOKS[@]}"; do
        echo "calling \"$fn\""
        eval $fn || true
    done
}

function kgr_tc_write() {
    logger "$*"
    echo "$*"
}

function kgr_tc_init() {
    trap "[ \$? -ne 0 ] && echo TEST FAILED while executing \'\$BASH_COMMAND\', EXITING; call_recovery_hooks" EXIT
    kgr_tc_write "$1"
    if kgr_in_progress; then
        kgr_tc_write "ERROR kGraft patching in progress, cannot start test"
	exit 22 # means SKIPPED in CTCS2 terminology
    fi
}

function kgr_tc_milestone() {
    kgr_tc_write "***" "$*"
}

function kgr_tc_abort() {
    kgr_tc_write "TEST CASE ABORT" "$*"
    exit 1
}

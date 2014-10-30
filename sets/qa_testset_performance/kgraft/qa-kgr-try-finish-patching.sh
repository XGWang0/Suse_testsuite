function try_to_finish_patching {
    pushd /proc
    for PID in [0-9]*; do
       if test "X$(cat ${PID}/kgr_in_progress)" == X1; then
           kill -STOP ${PID}
           kill -CONT ${PID}
       fi
    done
    unset PIDS
    for PID in [0-9]*; do
        if test "X$(cat ${PID}/kgr_in_progress)" == X1; then
            COMM="$(cat ${PID}/comm)"
            echo "$COMM (${PID}) still in progress:"
	    cat ${PID}/stack
	    echo -e "======================\n"
            PIDS="$PIDS $PID"
        fi
    done
    if test -z "${PIDS}"; then
	echo "NO prcess is kgr_in_progress"
    else
        echo "Some process still is kgr_in_progress"
        echo "Manully fixed by yourself"
    fi
    popd
}

try_to_finish_patching

declare -a WORKLOAD_LIST
function add_workload {
    [ -z "$1" ]  && echo "WARNING: no parameters passed to $FUNCNAME"
    case $1 in
        cpu):;;
        mem):;;
        *) echo "WARNING: $1 dose not exist";return 1;;
    esac
    WORKLOAD_LIST[${#WORKLOAD_LIST[*]}]="$1"
}

function start_workload {
    for w in "${WORKLOAD_LIST[@]}"; do
        echo "start ${w}"
        eval workload_$w
    done
}

function workload_A_start {
    local pid
    cat /dev/urandom > /dev/null &
    pid=$!
    if test "X$(type -t push_recovery_fn)" == "Xfunction"; then
        push_recovery_fn "kill $pid"
    fi
}

function workload_cpu {
    echo "WORKLOAD cpu"

    for i in $(seq 1 $(nproc)); do
        workload_A_start
    done
}

function workload_mem {
    local pid
    local CHIMEM_BIN='/usr/share/qa/qa_test_kgraft/bin/chimem'
    echo "WORKLOAD memory"

    ${CHIMEM_BIN} &
    pid=$!
    if test "X$(type -t push_recovery_fn)" == "Xfunction"; then
        push_recovery_fn "kill $pid"
    fi    
}

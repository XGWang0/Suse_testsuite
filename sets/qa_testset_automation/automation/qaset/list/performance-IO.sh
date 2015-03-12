#!/bin/bash

__import qavm/sq-util.sh
__import set/performance.set


PERFORMANCE_IO_L0=(
    reaim_ioperf
    iozone_bigmem_basic
    tiobench_basic
    pgbench_small
    bonniepp
    bonniepp_fsync
    sysbench_oltp
)

PERFORMANCE_IO_L1=(
    dbench4
    dbench4_fsync
    pgbench_medium
    pgbench_large
)

PERFORMANCE_IO_L100=(
    dbench4_nfs
    dbench4_nfs4
)

function performance_io_add_to_list {
    if test $# -lt 4; then
        sq_error "${FUNCNAME} need 4 args"
        return
    fi

    local target_list=$1
    local source_list=$2
    local fs_list=$3
    local iterate=$4

    local source
    local fs
    local i
    local l_i
    local j
    local l_j
    local k
    local l_k
    local last


    eval "l_i=\${#${source_list}[@]}"
    eval "l_j=\${#${fs_list}[@]}"
    i=0
    while test $i -lt ${l_i};do
        eval "source=\${${source_list}[$i]}"
        j=0
        while test $j -lt ${l_j};do
            eval "fs=\${${fs_list}[$j]}"
            k=0
            eval "last=\${#${target_list}[@]}"
            while test $k -lt $iterate; do
                eval "${target_list}[$last]=${source}_${fs}"
                let k++
                let last++
            done
            let j++
        done
        let i++
    done
}

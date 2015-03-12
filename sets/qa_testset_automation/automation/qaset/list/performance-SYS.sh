#!/bin/bash

# The default list of general system performance test
SQ_TEST_RUN_LIST=(
    siege
    siege
    siege

    sysbench_sys
    sysbench_sys
    sysbench_sys

    libmicro_bench
    libmicro_bench
    libmicro_bench

    lmbench_bench
    lmbench_bench
    lmbench_bench

    kernbench
    kernbench
    kernbench

    #one time is OK because netperf has a good statitics process.
    netperf_loop4
    netperf_loop6

    #manual seting up of server is needed.
    #netperf_fiber4
    #netperf_fiber6
)

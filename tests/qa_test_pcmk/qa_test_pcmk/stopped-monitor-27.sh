#!/bin/bash
#Stopped Monitor - unmanaged stopped multi-up (target-role=
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-27	"Stopped Monitor - unmanaged stopped multi-up (target-role="Started")"
test_results
clean_empty

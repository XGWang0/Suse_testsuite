#!/bin/bash
#Stopped Monitor - unmanaged stopped multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-25	"Stopped Monitor - unmanaged stopped multi-up"
test_results
clean_empty

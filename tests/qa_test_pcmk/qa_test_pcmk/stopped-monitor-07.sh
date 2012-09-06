#!/bin/bash
#Stopped Monitor - start unmanaged multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-07	"Stopped Monitor - start unmanaged multi-up"
test_results
clean_empty

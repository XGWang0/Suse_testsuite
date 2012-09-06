#!/bin/bash
#Stopped Monitor - stopped single-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-21	"Stopped Monitor - stopped single-up"
test_results
clean_empty

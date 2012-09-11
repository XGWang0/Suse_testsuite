#!/bin/bash
#Stopped Monitor - stopped multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-22	"Stopped Monitor - stopped multi-up"
test_results
clean_empty

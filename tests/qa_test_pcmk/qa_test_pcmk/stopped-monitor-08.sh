#!/bin/bash
#Stopped Monitor - migrate
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-08	"Stopped Monitor - migrate"
test_results
clean_empty

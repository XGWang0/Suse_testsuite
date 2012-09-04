#!/bin/bash
#Stopped Monitor - unmanaged multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-06	"Stopped Monitor - unmanaged multi-up"
test_results
clean_empty

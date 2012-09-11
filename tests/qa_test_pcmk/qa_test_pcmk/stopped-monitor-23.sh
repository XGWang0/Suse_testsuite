#!/bin/bash
#Stopped Monitor - start stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-23	"Stopped Monitor - start stopped"
test_results
clean_empty

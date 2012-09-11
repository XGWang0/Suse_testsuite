#!/bin/bash
#Stopped Monitor - new node stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-31	"Stopped Monitor - new node stopped"
test_results
clean_empty

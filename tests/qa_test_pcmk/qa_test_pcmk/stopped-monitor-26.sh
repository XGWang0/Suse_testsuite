#!/bin/bash
#Stopped Monitor - start unmanaged stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-26	"Stopped Monitor - start unmanaged stopped"
test_results
clean_empty

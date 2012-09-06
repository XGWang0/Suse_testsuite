#!/bin/bash
#Stopped Monitor - start unmanaged
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-05	"Stopped Monitor - start unmanaged"
test_results
clean_empty

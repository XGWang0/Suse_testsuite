#!/bin/bash
#Stopped Monitor - started multi-up
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-02	"Stopped Monitor - started multi-up"
test_results
clean_empty

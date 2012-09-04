#!/bin/bash
#Stopped Monitor - unmanaged started multi-up (targer-role=
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test stopped-monitor-12	"Stopped Monitor - unmanaged started multi-up (targer-role="Stopped")"
test_results
clean_empty

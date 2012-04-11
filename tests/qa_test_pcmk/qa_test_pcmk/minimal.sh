#!/bin/bash
#Placement Strategy - minimal
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test minimal     "Placement Strategy - minimal"
test_results
clean_empty

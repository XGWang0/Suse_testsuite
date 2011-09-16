#!/bin/bash
#Ensure resources that depend on the master don't get allocated until the master does
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-depend "Ensure resources that depend on the master don't get allocated until the master does"
test_results
clean_empty

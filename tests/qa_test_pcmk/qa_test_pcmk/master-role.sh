#!/bin/bash
#Prevent target-role from promoting more than master-max instances
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-role "Prevent target-role from promoting more than master-max instances"
test_results
clean_empty

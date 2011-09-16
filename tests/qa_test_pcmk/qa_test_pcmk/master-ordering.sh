#!/bin/bash
#Prevent resources from starting that need a master
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-ordering "Prevent resources from starting that need a master"
test_results
clean_empty

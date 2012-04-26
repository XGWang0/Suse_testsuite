#!/bin/bash
#Ensure clones don't get stopped/demoted because a dependant must stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test coloc-clone-stays-active "Ensure clones don't get stopped/demoted because a dependant must stop"
test_results
clean_empty

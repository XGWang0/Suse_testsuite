#!/bin/bash
#Resource Recover - multiple - restart
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-rsc-6 "Resource Recover - multiple - restart"
test_results
clean_empty

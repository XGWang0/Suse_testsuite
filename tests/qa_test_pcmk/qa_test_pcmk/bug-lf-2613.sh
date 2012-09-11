#!/bin/bash
#Move group on failure
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2613 "Move group on failure"
test_results
clean_empty

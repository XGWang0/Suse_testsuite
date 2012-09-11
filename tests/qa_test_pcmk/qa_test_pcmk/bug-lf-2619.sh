#!/bin/bash
#Move group on clone failure
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2619 "Move group on clone failure"
test_results
clean_empty

#!/bin/bash
#Non-unique clone (stop)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc10 "Non-unique clone (stop)"
test_results
clean_empty

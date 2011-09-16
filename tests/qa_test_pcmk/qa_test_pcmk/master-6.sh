#!/bin/bash
#Promoted -> Promoted (2)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-6 "Promoted -> Promoted (2)"
test_results
clean_empty

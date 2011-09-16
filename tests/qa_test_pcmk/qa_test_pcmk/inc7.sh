#!/bin/bash
#Clone colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc7 "Clone colocation"
test_results
clean_empty

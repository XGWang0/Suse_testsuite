#!/bin/bash
#Move master based on failure of colocated group
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-move "Move master based on failure of colocated group"
test_results
clean_empty

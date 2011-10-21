#!/bin/bash


#Migration in a starting stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-start "Migration in a starting stack"
test_results
clean_empty


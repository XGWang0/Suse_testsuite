#!/bin/bash


#Migration in a complex starting stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-start-complex "Migration in a complex starting stack"
test_results
clean_empty


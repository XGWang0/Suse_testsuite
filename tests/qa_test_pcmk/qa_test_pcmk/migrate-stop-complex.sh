#!/bin/bash


#Migration in a complex stopping stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-stop-complex "Migration in a complex stopping stack"
test_results
clean_empty


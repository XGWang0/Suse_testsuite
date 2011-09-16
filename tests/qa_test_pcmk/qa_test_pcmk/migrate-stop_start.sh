#!/bin/bash
#Migration in a restarting stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-stop_start "Migration in a restarting stack"
test_results
clean_empty

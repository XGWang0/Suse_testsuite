#!/bin/bash
#Migration in a stopping stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-stop "Migration in a stopping stack"
test_results
clean_empty

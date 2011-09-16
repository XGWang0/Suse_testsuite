#!/bin/bash
#Migration after Fencing
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fencing "Migration after Fencing"
test_results
clean_empty

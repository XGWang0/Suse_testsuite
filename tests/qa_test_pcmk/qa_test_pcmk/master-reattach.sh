#!/bin/bash
#Re-attach to a running master
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-reattach "Re-attach to a running master"
test_results
clean_empty

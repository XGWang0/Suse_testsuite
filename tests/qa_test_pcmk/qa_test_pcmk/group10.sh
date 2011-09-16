#!/bin/bash
#Group partial recovery
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group10 "Group partial recovery"
test_results
clean_empty

#!/bin/bash
#Group recovery
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group9 "Group recovery"
test_results
clean_empty

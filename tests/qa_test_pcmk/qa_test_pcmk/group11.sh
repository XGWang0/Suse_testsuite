#!/bin/bash
#Group target_role
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group11 "Group target_role"
test_results
clean_empty

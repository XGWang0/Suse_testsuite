#!/bin/bash
#Group colocation (cant run)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test group13 "Group colocation (cant run)"
test_results
clean_empty

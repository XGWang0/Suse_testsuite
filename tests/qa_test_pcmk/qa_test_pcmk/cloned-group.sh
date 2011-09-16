#!/bin/bash
#Make sure only the correct number of cloned groups are started
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test cloned-group "Make sure only the correct number of cloned groups are started"
test_results
clean_empty

#!/bin/bash
#Make sure promote/demote pseudo actions are created correctly
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-pseudo "Make sure promote/demote pseudo actions are created correctly"
test_results
clean_empty

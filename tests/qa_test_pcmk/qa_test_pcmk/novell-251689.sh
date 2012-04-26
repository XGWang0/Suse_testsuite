#!/bin/bash
#Resource definition change + target_role=stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-251689 "Resource definition change + target_role=stopped"
test_results
clean_empty

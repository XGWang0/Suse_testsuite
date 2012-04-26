#!/bin/bash
#Dependancy on partially active group - stop ocfs:*
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2422 "Dependancy on partially active group - stop ocfs:*"
test_results
clean_empty

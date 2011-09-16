#!/bin/bash
#Dont retry failed demote actions (notify=false)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-failed-demote-2 "Dont retry failed demote actions (notify=false)"
test_results
clean_empty

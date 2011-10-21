#!/bin/bash


#Dont retry failed demote actions
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-failed-demote "Dont retry failed demote actions"
test_results
clean_empty


#!/bin/bash
#Completed migration
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-success   "Completed migration"
test_results
clean_empty

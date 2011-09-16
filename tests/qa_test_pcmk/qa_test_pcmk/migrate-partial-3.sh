#!/bin/bash
#Successful migrate_to only, target down
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-partial-3 "Successful migrate_to only, target down"
test_results
clean_empty

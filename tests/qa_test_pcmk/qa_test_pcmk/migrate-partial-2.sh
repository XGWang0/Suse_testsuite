#!/bin/bash


#Successful migrate_to only
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-partial-2 "Successful migrate_to only"
test_results
clean_empty


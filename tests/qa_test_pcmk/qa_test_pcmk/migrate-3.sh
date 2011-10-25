#!/bin/bash


#Migrate (failed migrate_to)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-3 "Migrate (failed migrate_to)"
test_results
clean_empty


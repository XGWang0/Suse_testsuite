#!/bin/bash


#Migrate (failed migrate_from)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-4 "Migrate (failed migrate_from)"
test_results
clean_empty


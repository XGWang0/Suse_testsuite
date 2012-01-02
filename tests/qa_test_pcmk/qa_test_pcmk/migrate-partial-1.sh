#!/bin/bash


#Completed migration, missing stop on source
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-partial-1 "Completed migration, missing stop on source"
test_results
clean_empty


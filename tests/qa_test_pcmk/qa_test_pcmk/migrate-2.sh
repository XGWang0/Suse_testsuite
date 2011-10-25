#!/bin/bash


#Migrate (stable)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-2 "Migrate (stable)"
test_results
clean_empty


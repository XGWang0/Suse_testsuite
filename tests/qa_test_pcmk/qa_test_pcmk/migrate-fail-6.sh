#!/bin/bash


#Failed migrate_to
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-6 "Failed migrate_to"
test_results
clean_empty


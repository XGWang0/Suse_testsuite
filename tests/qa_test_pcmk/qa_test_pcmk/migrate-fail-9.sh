#!/bin/bash


#Failed migrate_to + stop on source and target
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-9 "Failed migrate_to + stop on source and target"
test_results
clean_empty

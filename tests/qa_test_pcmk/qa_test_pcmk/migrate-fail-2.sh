#!/bin/bash


#Failed migrate_from
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-2 "Failed migrate_from"
test_results
clean_empty


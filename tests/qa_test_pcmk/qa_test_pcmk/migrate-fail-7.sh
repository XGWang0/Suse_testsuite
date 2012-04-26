#!/bin/bash
#Failed migrate_to + stop on source
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-7 "Failed migrate_to + stop on source"
test_results
clean_empty

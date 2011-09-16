#!/bin/bash
#Failed migrate_from + stop on source
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-3 "Failed migrate_from + stop on source"
test_results
clean_empty

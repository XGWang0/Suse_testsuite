#!/bin/bash
#Failed migrate_to + stop on target - ideally we wouldn't need to re-stop on target
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-fail-8 "Failed migrate_to + stop on target - ideally we wouldn't need to re-stop on target"
test_results
clean_empty

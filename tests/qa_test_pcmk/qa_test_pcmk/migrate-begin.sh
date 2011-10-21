#!/bin/bash


#Normal migration
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-begin     "Normal migration"
test_results
clean_empty


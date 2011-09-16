#!/bin/bash
#Migrate (migrate)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-1 "Migrate (migrate)"
test_results
clean_empty

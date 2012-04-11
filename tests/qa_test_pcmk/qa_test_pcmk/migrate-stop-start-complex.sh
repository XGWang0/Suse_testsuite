#!/bin/bash
#Migration in a complex moving stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test migrate-stop-start-complex "Migration in a complex moving stack"
test_results
clean_empty

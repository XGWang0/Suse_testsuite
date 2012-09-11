#!/bin/bash
#Start the correct monitor operation for unmanaged masters
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-unmanaged-monitor "Start the correct monitor operation for unmanaged masters"
test_results
clean_empty

#!/bin/bash
#Ensure role is preserved for unmanaged resources
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test unmanaged-master "Ensure role is preserved for unmanaged resources"
test_results
clean_empty

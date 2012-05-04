#!/bin/bash
#Ordering when actions depends on demoting a slave resource
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-demote "Ordering when actions depends on demoting a slave resource"
test_results
clean_empty

#!/bin/bash
#Don't include master score if it would prevent allocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-allow-start "Don't include master score if it would prevent allocation"
test_results
clean_empty

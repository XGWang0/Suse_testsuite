#!/bin/bash
#No quorum - start anyway
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-4 "No quorum - start anyway"
test_results
clean_empty

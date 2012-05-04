#!/bin/bash
#No quorum - freeze
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-2 "No quorum - freeze"
test_results
clean_empty

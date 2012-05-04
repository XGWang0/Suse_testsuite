#!/bin/bash
#Use-after-free in native_merge_weights
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test use-after-free-merge "Use-after-free in native_merge_weights"
test_results
clean_empty

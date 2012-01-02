#!/bin/bash


#No quorum - start anyway (clone)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-6 "No quorum - start anyway (clone)"
test_results
clean_empty


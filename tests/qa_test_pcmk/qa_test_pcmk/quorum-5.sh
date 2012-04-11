#!/bin/bash
#No quorum - start anyway (group)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test quorum-5 "No quorum - start anyway (group)"
test_results
clean_empty

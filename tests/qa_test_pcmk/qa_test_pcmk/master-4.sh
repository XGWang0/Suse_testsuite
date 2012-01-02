#!/bin/bash


#Started -> Promote : master location
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-4 "Started -> Promote : master location"
test_results
clean_empty


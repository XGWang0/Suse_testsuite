#!/bin/bash


#Don't shuffle clone instances
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-n-387749 "Don't shuffle clone instances"
test_results
clean_empty


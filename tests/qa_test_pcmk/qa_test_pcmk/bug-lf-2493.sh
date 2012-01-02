#!/bin/bash


#Don't imply colocation requirements when applying ordering constraints with clones
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2493 "Don't imply colocation requirements when applying ordering constraints with clones"
test_results
clean_empty


#!/bin/bash
#Dont shuffle clones due to colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2160 "Dont shuffle clones due to colocation"
test_results
clean_empty

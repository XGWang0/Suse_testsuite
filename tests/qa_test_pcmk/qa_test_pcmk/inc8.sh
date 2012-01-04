#!/bin/bash


#Clone anti-colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc8 "Clone anti-colocation"
test_results
clean_empty


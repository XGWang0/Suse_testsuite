#!/bin/bash


#Resource Sets - Master
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc-sets-master "Resource Sets - Master"
test_results
clean_empty


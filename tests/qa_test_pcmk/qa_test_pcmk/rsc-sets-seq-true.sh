#!/bin/bash


#Resource Sets - sequential=false
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc-sets-seq-true "Resource Sets - sequential=false"
test_results
clean_empty


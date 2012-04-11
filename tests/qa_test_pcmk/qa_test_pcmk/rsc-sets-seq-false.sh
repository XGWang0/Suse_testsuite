#!/bin/bash
#Resource Sets - sequential=true
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc-sets-seq-false "Resource Sets - sequential=true"
test_results
clean_empty

#!/bin/bash


#Resource Sets - Clone
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc-sets-clone "Resource Sets - Clone"
test_results
clean_empty


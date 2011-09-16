#!/bin/bash
#Primitive colocation with clones
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc11 "Primitive colocation with clones"
test_results
clean_empty

#!/bin/bash


#Must (running + move)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep4  "Must (running + move)"
test_results
clean_empty


#!/bin/bash


#Must (but cant)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rsc_dep10 "Must (but cant)"
test_results
clean_empty


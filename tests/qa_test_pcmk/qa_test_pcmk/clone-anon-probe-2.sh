#!/bin/bash


#Avoid needless re-probing of anonymous clones
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-anon-probe-2 "Avoid needless re-probing of anonymous clones"
test_results
clean_empty


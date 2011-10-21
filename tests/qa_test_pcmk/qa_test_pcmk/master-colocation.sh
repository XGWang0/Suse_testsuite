#!/bin/bash


#Allow master instances placemaker to be influenced by colocation constraints
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-colocation "Allow master instances placemaker to be influenced by colocation constraints"
test_results
clean_empty


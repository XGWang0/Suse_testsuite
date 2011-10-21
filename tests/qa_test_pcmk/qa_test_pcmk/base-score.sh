#!/bin/bash


#Set a node's default score for all nodes
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test base-score "Set a node's default score for all nodes"
test_results
clean_empty


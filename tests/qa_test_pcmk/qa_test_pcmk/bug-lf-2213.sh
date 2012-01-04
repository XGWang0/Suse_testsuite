#!/bin/bash


#clone-node-max enforcement for cloned groups
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2213 "clone-node-max enforcement for cloned groups"
test_results
clean_empty


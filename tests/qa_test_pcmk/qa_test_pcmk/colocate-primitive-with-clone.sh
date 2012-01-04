#!/bin/bash


#Optional colocation with a clone
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test colocate-primitive-with-clone "Optional colocation with a clone"
test_results
clean_empty


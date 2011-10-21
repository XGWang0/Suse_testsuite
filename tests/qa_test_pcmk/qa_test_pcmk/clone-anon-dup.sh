#!/bin/bash


#Bug LF2087 - Correctly parse the state of anonymous clones that are active more than once per node
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-anon-dup "Bug LF2087 - Correctly parse the state of anonymous clones that are active more than once per node"
test_results
clean_empty


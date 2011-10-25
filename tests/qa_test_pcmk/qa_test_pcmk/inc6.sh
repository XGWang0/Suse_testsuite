#!/bin/bash


#Inter-incarnation ordering, silent restart, stop, move (restart 2)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc6 "Inter-incarnation ordering, silent restart, stop, move (restart 2)"
test_results
clean_empty


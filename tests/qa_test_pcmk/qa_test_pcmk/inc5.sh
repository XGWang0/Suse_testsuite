#!/bin/bash
#Inter-incarnation ordering, silent restart, stop, move (restart 1)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc5 "Inter-incarnation ordering, silent restart, stop, move (restart 1)"
test_results
clean_empty

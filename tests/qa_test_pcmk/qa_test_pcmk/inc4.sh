#!/bin/bash
#Inter-incarnation ordering, silent restart, stop, move (ordered)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc4 "Inter-incarnation ordering, silent restart, stop, move (ordered)"
test_results
clean_empty

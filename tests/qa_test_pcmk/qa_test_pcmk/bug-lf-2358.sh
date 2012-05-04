#!/bin/bash
#Master-Master anti-colocation
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-2358 "Master-Master anti-colocation"
test_results
clean_empty

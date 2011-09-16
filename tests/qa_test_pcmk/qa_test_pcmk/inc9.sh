#!/bin/bash
#Non-unique clone
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc9 "Non-unique clone"
test_results
clean_empty

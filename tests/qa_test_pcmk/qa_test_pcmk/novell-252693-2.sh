#!/bin/bash
#Migration in a starting stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-252693-2 "Migration in a starting stack"
test_results
clean_empty

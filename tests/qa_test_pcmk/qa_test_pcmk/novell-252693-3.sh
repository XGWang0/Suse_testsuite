#!/bin/bash


#Non-Migration in a starting and stopping stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-252693-3 "Non-Migration in a starting and stopping stack"
test_results
clean_empty


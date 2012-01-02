#!/bin/bash


#Migration in a stopping stack
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-252693 "Migration in a stopping stack"
test_results
clean_empty


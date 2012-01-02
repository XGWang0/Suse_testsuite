#!/bin/bash


#Demote/Promote ordering
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-239082 "Demote/Promote ordering"
test_results
clean_empty


#!/bin/bash
#Incarnation silent restart, stop, move
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test inc2 "Incarnation silent restart, stop, move"
test_results
clean_empty

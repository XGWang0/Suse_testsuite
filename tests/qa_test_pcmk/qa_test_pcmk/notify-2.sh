#!/bin/bash
#Notify simple, confirm
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test notify-2 "Notify simple, confirm"
test_results
clean_empty

#!/bin/bash
#Notify reference
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test notify-0 "Notify reference"
test_results
clean_empty

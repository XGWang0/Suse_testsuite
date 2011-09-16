#!/bin/bash
#Ensure correct target_rc for reprobe of inactive resources
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test reprobe-target_rc "Ensure correct target_rc for reprobe of inactive resources"
test_results
clean_empty

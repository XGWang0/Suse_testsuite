#!/bin/bash
#Node Recover - CRM down w/ group - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-11 "Node Recover - CRM down w/ group - fence   "
test_results
clean_empty

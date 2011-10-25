#!/bin/bash


#Node Recover - CRM down - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-6 "Node Recover - CRM down  - fence   "
test_results
clean_empty


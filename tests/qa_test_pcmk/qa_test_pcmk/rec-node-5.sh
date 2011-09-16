#!/bin/bash
#Node Recover - CRM down - no fence
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-5 "Node Recover - CRM down  - no fence"
test_results
clean_empty

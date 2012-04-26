#!/bin/bash
#Serialize all stonith's
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-14 "Serialize all stonith's"
test_results
clean_empty

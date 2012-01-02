#!/bin/bash


#Node Recover - failed resource + shutdown - fence 
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test rec-node-13 "Node Recover - failed resource + shutdown - fence   "
test_results
clean_empty


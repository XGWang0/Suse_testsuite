#!/bin/bash
#Probe the correct (anonymous) clone instance for each node
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-anon-probe-1 "Probe the correct (anonymous) clone instance for each node"
test_results
clean_empty

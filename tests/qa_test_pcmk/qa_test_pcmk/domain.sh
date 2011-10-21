#!/bin/bash


#Failover domains
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test domain "Failover domains"
test_results
clean_empty


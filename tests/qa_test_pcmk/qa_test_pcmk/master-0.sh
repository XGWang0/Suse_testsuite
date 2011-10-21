#!/bin/bash


#Stopped -> Slave
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-0 "Stopped -> Slave"
test_results
clean_empty


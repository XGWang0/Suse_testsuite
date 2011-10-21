#!/bin/bash


#Serialize a set of resources without inhibiting migration
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-serialize-set "Serialize a set of resources without inhibiting migration"
test_results
clean_empty


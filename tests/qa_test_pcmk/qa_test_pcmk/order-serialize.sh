#!/bin/bash
#Serialize resources without inhibiting migration
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-serialize "Serialize resources without inhibiting migration"
test_results
clean_empty

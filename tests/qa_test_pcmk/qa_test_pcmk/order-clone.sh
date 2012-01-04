#!/bin/bash


#Clone ordering should be able to prevent startup of dependant clones
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-clone "Clone ordering should be able to prevent startup of dependant clones"
test_results
clean_empty


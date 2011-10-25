#!/bin/bash


#Recovery of groups depending on master/slave
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1572-1 "Recovery of groups depending on master/slave"
test_results
clean_empty


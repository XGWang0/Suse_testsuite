#!/bin/bash

#OSDL 1484 - on_fail=stop
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test 1484 "OSDL 1484 - on_fail=stop"
test_results
clean_empty


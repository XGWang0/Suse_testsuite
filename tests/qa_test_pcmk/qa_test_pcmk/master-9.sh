#!/bin/bash
#Stopped + Promotable + No quorum
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test master-9 "Stopped + Promotable + No quorum"
test_results
clean_empty

#!/bin/bash
#Ticket - Master (loss-policy=stop, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-1 "Ticket - Master (loss-policy=stop, initial)"
test_results
clean_empty

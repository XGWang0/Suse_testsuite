#!/bin/bash
#Ticket - Group (loss-policy=stop, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-1 "Ticket - Group (loss-policy=stop, initial)"
test_results
clean_empty

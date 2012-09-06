#!/bin/bash
#Ticket - Group (loss-policy=demote, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-4 "Ticket - Group (loss-policy=demote, initial)"
test_results
clean_empty

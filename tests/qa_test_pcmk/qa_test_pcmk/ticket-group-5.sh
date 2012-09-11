#!/bin/bash
#Ticket - Group (loss-policy=demote, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-5 "Ticket - Group (loss-policy=demote, granted)"
test_results
clean_empty

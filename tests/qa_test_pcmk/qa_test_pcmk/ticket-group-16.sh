#!/bin/bash
#Ticket - Group (loss-policy=demote, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-16 "Ticket - Group (loss-policy=demote, standby, granted)"
test_results
clean_empty

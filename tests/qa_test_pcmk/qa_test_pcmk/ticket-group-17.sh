#!/bin/bash
#Ticket - Group (loss-policy=demote, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-17 "Ticket - Group (loss-policy=demote, granted, standby)"
test_results
clean_empty

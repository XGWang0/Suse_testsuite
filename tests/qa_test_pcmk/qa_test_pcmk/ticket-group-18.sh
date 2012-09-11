#!/bin/bash
#Ticket - Group (loss-policy=demote, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-18 "Ticket - Group (loss-policy=demote, standby, revoked)"
test_results
clean_empty

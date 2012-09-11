#!/bin/bash
#Ticket - Group (loss-policy=demote, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-6 "Ticket - Group (loss-policy=demote, revoked)"
test_results
clean_empty

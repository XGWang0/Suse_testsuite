#!/bin/bash
#Ticket - Group (loss-policy=stop, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-15 "Ticket - Group (loss-policy=stop, standby, revoked)"
test_results
clean_empty

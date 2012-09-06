#!/bin/bash
#Ticket - Group (loss-policy=fence, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-21 "Ticket - Group (loss-policy=fence, standby, revoked)"
test_results
clean_empty

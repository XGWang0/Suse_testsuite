#!/bin/bash
#Ticket - Group (loss-policy=fence, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-9 "Ticket - Group (loss-policy=fence, revoked)"
test_results
clean_empty

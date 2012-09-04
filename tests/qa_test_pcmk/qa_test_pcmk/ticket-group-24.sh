#!/bin/bash
#Ticket - Group (loss-policy=freeze, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-24 "Ticket - Group (loss-policy=freeze, standby, revoked)"
test_results
clean_empty

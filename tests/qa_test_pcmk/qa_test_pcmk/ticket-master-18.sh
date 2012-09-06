#!/bin/bash
#Ticket - Master (loss-policy=demote, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-18 "Ticket - Master (loss-policy=demote, standby, revoked)"
test_results
clean_empty

#!/bin/bash
#Ticket - Master (loss-policy=demote, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-6 "Ticket - Master (loss-policy=demote, revoked)"
test_results
clean_empty

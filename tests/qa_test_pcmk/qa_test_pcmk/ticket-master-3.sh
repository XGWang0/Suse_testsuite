#!/bin/bash
#Ticket - Master (loss-policy-stop, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-3 "Ticket - Master (loss-policy-stop, revoked)"
test_results
clean_empty

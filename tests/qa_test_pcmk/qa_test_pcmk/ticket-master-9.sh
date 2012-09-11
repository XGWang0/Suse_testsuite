#!/bin/bash
#Ticket - Master (loss-policy=fence, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-9 "Ticket - Master (loss-policy=fence, revoked)"
test_results
clean_empty

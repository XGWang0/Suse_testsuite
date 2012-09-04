#!/bin/bash
#Ticket - Master (loss-policy=fence, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-21 "Ticket - Master (loss-policy=fence, standby, revoked)"
test_results
clean_empty

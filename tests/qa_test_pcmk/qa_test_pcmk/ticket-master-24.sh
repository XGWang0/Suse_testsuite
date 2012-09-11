#!/bin/bash
#Ticket - Master (loss-policy=freeze, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-24 "Ticket - Master (loss-policy=freeze, standby, revoked)"
test_results
clean_empty

#!/bin/bash
#Ticket - Master (loss-policy=freeze, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-12 "Ticket - Master (loss-policy=freeze, revoked)"
test_results
clean_empty

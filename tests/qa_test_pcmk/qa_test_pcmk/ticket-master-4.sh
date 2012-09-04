#!/bin/bash
#Ticket - Master (loss-policy=demote, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-4 "Ticket - Master (loss-policy=demote, initial)"
test_results
clean_empty

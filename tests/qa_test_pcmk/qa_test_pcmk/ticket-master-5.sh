#!/bin/bash
#Ticket - Master (loss-policy=demote, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-5 "Ticket - Master (loss-policy=demote, granted)"
test_results
clean_empty

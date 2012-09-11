#!/bin/bash
#Ticket - Master (loss-policy=demote, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-16 "Ticket - Master (loss-policy=demote, standby, granted)"
test_results
clean_empty

#!/bin/bash
#Ticket - Master (loss-policy=demote, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-17 "Ticket - Master (loss-policy=demote, granted, standby)"
test_results
clean_empty

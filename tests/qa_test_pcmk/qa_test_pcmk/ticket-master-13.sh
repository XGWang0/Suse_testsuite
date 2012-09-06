#!/bin/bash
#Ticket - Master (loss-policy=stop, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-13 "Ticket - Master (loss-policy=stop, standby, granted)"
test_results
clean_empty

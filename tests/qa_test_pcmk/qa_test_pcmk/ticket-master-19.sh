#!/bin/bash
#Ticket - Master (loss-policy=fence, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-19 "Ticket - Master (loss-policy=fence, standby, granted)"
test_results
clean_empty

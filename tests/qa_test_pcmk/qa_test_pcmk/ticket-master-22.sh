#!/bin/bash
#Ticket - Master (loss-policy=freeze, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-22 "Ticket - Master (loss-policy=freeze, standby, granted)"
test_results
clean_empty

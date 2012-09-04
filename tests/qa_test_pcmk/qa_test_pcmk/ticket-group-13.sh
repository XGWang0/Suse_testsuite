#!/bin/bash
#Ticket - Group (loss-policy=stop, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-13 "Ticket - Group (loss-policy=stop, standby, granted)"
test_results
clean_empty

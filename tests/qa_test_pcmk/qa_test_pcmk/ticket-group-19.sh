#!/bin/bash
#Ticket - Group (loss-policy=fence, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-19 "Ticket - Group (loss-policy=fence, standby, granted)"
test_results
clean_empty

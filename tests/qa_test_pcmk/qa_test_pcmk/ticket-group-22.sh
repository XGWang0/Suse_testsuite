#!/bin/bash
#Ticket - Group (loss-policy=freeze, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-22 "Ticket - Group (loss-policy=freeze, standby, granted)"
test_results
clean_empty

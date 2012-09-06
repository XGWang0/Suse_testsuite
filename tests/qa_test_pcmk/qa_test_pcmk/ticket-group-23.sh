#!/bin/bash
#Ticket - Group (loss-policy=freeze, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-23 "Ticket - Group (loss-policy=freeze, granted, standby)"
test_results
clean_empty

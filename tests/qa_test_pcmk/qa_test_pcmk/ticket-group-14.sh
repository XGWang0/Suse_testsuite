#!/bin/bash
#Ticket - Group (loss-policy=stop, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-14 "Ticket - Group (loss-policy=stop, granted, standby)"
test_results
clean_empty

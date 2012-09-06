#!/bin/bash
#Ticket - Group (loss-policy=fence, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-20 "Ticket - Group (loss-policy=fence, granted, standby)"
test_results
clean_empty

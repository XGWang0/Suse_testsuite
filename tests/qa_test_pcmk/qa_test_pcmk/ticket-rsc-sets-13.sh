#!/bin/bash
#Ticket - Resource sets (2 tickets, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-13 "Ticket - Resource sets (2 tickets, granted, standby)"
test_results
clean_empty

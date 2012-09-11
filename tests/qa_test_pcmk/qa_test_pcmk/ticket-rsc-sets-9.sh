#!/bin/bash
#Ticket - Resource sets (1 ticket, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-9 "Ticket - Resource sets (1 ticket, granted, standby)"
test_results
clean_empty

#!/bin/bash
#Ticket - Resource sets (2 tickets, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-12 "Ticket - Resource sets (2 tickets, standby, granted)"
test_results
clean_empty

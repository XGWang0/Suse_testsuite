#!/bin/bash
#Ticket - Resource sets (1 ticket, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-8 "Ticket - Resource sets (1 ticket, standby, granted)"
test_results
clean_empty

#!/bin/bash
#Ticket - Resource sets (2 tickets, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-4 "Ticket - Resource sets (2 tickets, initial)"
test_results
clean_empty

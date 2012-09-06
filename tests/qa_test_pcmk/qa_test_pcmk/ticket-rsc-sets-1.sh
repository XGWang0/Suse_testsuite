#!/bin/bash
#Ticket - Resource sets (1 ticket, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-1 "Ticket - Resource sets (1 ticket, initial)"
test_results
clean_empty

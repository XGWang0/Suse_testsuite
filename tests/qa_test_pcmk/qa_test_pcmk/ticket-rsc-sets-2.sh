#!/bin/bash
#Ticket - Resource sets (1 ticket, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-2 "Ticket - Resource sets (1 ticket, granted)"
test_results
clean_empty

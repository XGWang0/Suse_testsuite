#!/bin/bash
#Ticket - Resource sets (2 tickets, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-7 "Ticket - Resource sets (2 tickets, revoked)"
test_results
clean_empty

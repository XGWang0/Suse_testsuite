#!/bin/bash
#Ticket - Resource sets (1 ticket, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-3 "Ticket - Resource sets (1 ticket, revoked)"
test_results
clean_empty

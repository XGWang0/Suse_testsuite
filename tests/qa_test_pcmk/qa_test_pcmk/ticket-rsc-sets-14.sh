#!/bin/bash
#Ticket - Resource sets (2 tickets, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-14 "Ticket - Resource sets (2 tickets, standby, revoked)"
test_results
clean_empty

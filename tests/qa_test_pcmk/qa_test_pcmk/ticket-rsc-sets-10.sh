#!/bin/bash
#Ticket - Resource sets (1 ticket, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-rsc-sets-10 "Ticket - Resource sets (1 ticket, standby, revoked)"
test_results
clean_empty

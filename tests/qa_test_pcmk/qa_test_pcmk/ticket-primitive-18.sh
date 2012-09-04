#!/bin/bash
#Ticket - Primitive (loss-policy=demote, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-18 "Ticket - Primitive (loss-policy=demote, standby, revoked)"
test_results
clean_empty

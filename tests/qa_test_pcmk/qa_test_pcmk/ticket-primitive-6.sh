#!/bin/bash
#Ticket - Primitive (loss-policy=demote, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-6 "Ticket - Primitive (loss-policy=demote, revoked)"
test_results
clean_empty

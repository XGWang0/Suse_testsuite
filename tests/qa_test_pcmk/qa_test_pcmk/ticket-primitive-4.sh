#!/bin/bash
#Ticket - Primitive (loss-policy=demote, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-4 "Ticket - Primitive (loss-policy=demote, initial)"
test_results
clean_empty

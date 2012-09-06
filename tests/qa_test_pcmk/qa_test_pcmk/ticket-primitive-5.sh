#!/bin/bash
#Ticket - Primitive (loss-policy=demote, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-5 "Ticket - Primitive (loss-policy=demote, granted)"
test_results
clean_empty

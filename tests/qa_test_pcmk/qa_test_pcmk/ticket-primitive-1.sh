#!/bin/bash
#Ticket - Primitive (loss-policy=stop, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-1 "Ticket - Primitive (loss-policy=stop, initial)"
test_results
clean_empty

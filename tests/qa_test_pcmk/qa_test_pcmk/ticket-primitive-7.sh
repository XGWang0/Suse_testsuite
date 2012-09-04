#!/bin/bash
#Ticket - Primitive (loss-policy=fence, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-7 "Ticket - Primitive (loss-policy=fence, initial)"
test_results
clean_empty

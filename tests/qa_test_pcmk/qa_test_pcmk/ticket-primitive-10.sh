#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-10 "Ticket - Primitive (loss-policy=freeze, initial)"
test_results
clean_empty

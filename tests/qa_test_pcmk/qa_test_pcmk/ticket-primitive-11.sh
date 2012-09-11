#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-11 "Ticket - Primitive (loss-policy=freeze, granted)"
test_results
clean_empty

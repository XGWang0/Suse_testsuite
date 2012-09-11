#!/bin/bash
#Ticket - Primitive (loss-policy=stop, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-2 "Ticket - Primitive (loss-policy=stop, granted)"
test_results
clean_empty

#!/bin/bash
#Ticket - Primitive (loss-policy=fence, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-8 "Ticket - Primitive (loss-policy=fence, granted)"
test_results
clean_empty

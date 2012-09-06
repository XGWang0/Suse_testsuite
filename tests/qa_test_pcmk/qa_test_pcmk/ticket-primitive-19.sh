#!/bin/bash
#Ticket - Primitive (loss-policy=fence, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-19 "Ticket - Primitive (loss-policy=fence, standby, granted)"
test_results
clean_empty

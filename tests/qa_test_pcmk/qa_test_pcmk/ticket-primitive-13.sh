#!/bin/bash
#Ticket - Primitive (loss-policy=stop, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-13 "Ticket - Primitive (loss-policy=stop, standby, granted)"
test_results
clean_empty

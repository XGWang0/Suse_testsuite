#!/bin/bash
#Ticket - Primitive (loss-policy=demote, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-16 "Ticket - Primitive (loss-policy=demote, standby, granted)"
test_results
clean_empty

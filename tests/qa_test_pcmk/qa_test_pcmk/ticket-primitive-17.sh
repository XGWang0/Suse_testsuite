#!/bin/bash
#Ticket - Primitive (loss-policy=demote, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-17 "Ticket - Primitive (loss-policy=demote, granted, standby)"
test_results
clean_empty

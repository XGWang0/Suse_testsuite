#!/bin/bash
#Ticket - Primitive (loss-policy=stop, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-15 "Ticket - Primitive (loss-policy=stop, standby, revoked)"
test_results
clean_empty

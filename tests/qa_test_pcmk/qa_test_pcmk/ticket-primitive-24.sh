#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-24 "Ticket - Primitive (loss-policy=freeze, standby, revoked)"
test_results
clean_empty

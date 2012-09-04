#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-12 "Ticket - Primitive (loss-policy=freeze, revoked)"
test_results
clean_empty

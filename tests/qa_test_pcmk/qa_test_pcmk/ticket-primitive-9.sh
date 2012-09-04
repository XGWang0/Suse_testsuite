#!/bin/bash
#Ticket - Primitive (loss-policy=fence, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-9 "Ticket - Primitive (loss-policy=fence, revoked)"
test_results
clean_empty

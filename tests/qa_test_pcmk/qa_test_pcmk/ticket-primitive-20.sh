#!/bin/bash
#Ticket - Primitive (loss-policy=fence, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-20 "Ticket - Primitive (loss-policy=fence, granted, standby)"
test_results
clean_empty

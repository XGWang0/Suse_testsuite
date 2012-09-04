#!/bin/bash
#Ticket - Primitive (loss-policy=stop, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-14 "Ticket - Primitive (loss-policy=stop, granted, standby)"
test_results
clean_empty

#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-23 "Ticket - Primitive (loss-policy=freeze, granted, standby)"
test_results
clean_empty

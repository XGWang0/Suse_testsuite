#!/bin/bash
#Ticket - Primitive (loss-policy=freeze, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-primitive-22 "Ticket - Primitive (loss-policy=freeze, standby, granted)"
test_results
clean_empty

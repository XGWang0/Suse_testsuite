#!/bin/bash
#Ticket - Master (loss-policy=freeze, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-10 "Ticket - Master (loss-policy=freeze, initial)"
test_results
clean_empty

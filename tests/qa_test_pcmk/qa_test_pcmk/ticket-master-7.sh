#!/bin/bash
#Ticket - Master (loss-policy=fence, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-7 "Ticket - Master (loss-policy=fence, initial)"
test_results
clean_empty

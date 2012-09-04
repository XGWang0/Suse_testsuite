#!/bin/bash
#Ticket - Master (loss-policy=fence, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-8 "Ticket - Master (loss-policy=fence, granted)"
test_results
clean_empty

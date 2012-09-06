#!/bin/bash
#Ticket - Master (loss-policy=stop, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-2 "Ticket - Master (loss-policy=stop, granted)"
test_results
clean_empty

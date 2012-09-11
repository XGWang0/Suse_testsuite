#!/bin/bash
#Ticket - Master (loss-policy=freeze, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-11 "Ticket - Master (loss-policy=freeze, granted)"
test_results
clean_empty

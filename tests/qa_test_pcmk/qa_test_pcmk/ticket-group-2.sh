#!/bin/bash
#Ticket - Group (loss-policy=stop, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-2 "Ticket - Group (loss-policy=stop, granted)"
test_results
clean_empty

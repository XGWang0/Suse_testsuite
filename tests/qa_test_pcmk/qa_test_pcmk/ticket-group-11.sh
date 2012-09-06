#!/bin/bash
#Ticket - Group (loss-policy=freeze, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-11 "Ticket - Group (loss-policy=freeze, granted)"
test_results
clean_empty

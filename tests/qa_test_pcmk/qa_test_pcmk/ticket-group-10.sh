#!/bin/bash
#Ticket - Group (loss-policy=freeze, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-10 "Ticket - Group (loss-policy=freeze, initial)"
test_results
clean_empty

#!/bin/bash
#Ticket - Group (loss-policy=fence, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-7 "Ticket - Group (loss-policy=fence, initial)"
test_results
clean_empty

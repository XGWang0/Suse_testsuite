#!/bin/bash
#Ticket - Group (loss-policy=fence, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-group-8 "Ticket - Group (loss-policy=fence, granted)"
test_results
clean_empty

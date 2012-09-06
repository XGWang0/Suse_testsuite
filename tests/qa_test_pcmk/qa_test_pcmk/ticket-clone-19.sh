#!/bin/bash
#Ticket - Clone (loss-policy=fence, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-19 "Ticket - Clone (loss-policy=fence, standby, granted)"
test_results
clean_empty

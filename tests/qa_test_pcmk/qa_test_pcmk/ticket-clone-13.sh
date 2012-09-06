#!/bin/bash
#Ticket - Clone (loss-policy=stop, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-13 "Ticket - Clone (loss-policy=stop, standby, granted)"
test_results
clean_empty

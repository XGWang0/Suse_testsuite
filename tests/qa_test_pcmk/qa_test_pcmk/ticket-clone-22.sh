#!/bin/bash
#Ticket - Clone (loss-policy=freeze, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-22 "Ticket - Clone (loss-policy=freeze, standby, granted)"
test_results
clean_empty

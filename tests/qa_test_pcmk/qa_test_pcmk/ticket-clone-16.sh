#!/bin/bash
#Ticket - Clone (loss-policy=demote, standby, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-16 "Ticket - Clone (loss-policy=demote, standby, granted)"
test_results
clean_empty

#!/bin/bash
#Ticket - Clone (loss-policy=demote, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-17 "Ticket - Clone (loss-policy=demote, granted, standby)"
test_results
clean_empty

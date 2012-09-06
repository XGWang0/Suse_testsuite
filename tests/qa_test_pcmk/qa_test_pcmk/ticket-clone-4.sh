#!/bin/bash
#Ticket - Clone (loss-policy=demote, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-4 "Ticket - Clone (loss-policy=demote, initial)"
test_results
clean_empty

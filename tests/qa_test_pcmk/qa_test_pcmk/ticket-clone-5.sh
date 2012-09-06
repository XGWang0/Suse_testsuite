#!/bin/bash
#Ticket - Clone (loss-policy=demote, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-5 "Ticket - Clone (loss-policy=demote, granted)"
test_results
clean_empty

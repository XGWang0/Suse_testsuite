#!/bin/bash
#Ticket - Clone (loss-policy=stop, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-1 "Ticket - Clone (loss-policy=stop, initial)"
test_results
clean_empty

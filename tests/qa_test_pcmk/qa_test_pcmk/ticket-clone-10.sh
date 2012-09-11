#!/bin/bash
#Ticket - Clone (loss-policy=freeze, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-10 "Ticket - Clone (loss-policy=freeze, initial)"
test_results
clean_empty

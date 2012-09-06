#!/bin/bash
#Ticket - Clone (loss-policy=fence, initial)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-7 "Ticket - Clone (loss-policy=fence, initial)"
test_results
clean_empty

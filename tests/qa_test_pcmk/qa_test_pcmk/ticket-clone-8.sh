#!/bin/bash
#Ticket - Clone (loss-policy=fence, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-8 "Ticket - Clone (loss-policy=fence, granted)"
test_results
clean_empty

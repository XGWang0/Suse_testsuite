#!/bin/bash
#Ticket - Clone (loss-policy=stop, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-2 "Ticket - Clone (loss-policy=stop, granted)"
test_results
clean_empty

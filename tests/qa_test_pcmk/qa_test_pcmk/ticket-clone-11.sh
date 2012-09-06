#!/bin/bash
#Ticket - Clone (loss-policy=freeze, granted)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-11 "Ticket - Clone (loss-policy=freeze, granted)"
test_results
clean_empty

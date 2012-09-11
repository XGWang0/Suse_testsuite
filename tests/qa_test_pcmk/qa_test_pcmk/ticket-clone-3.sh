#!/bin/bash
#Ticket - Clone (loss-policy-stop, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-3 "Ticket - Clone (loss-policy-stop, revoked)"
test_results
clean_empty

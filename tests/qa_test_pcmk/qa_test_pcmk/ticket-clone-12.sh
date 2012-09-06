#!/bin/bash
#Ticket - Clone (loss-policy=freeze, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-12 "Ticket - Clone (loss-policy=freeze, revoked)"
test_results
clean_empty

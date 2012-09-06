#!/bin/bash
#Ticket - Clone (loss-policy=demote, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-6 "Ticket - Clone (loss-policy=demote, revoked)"
test_results
clean_empty

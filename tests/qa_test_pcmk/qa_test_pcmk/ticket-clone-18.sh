#!/bin/bash
#Ticket - Clone (loss-policy=demote, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-18 "Ticket - Clone (loss-policy=demote, standby, revoked)"
test_results
clean_empty

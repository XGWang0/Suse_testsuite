#!/bin/bash
#Ticket - Clone (loss-policy=stop, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-15 "Ticket - Clone (loss-policy=stop, standby, revoked)"
test_results
clean_empty

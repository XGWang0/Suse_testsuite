#!/bin/bash
#Ticket - Clone (loss-policy=fence, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-21 "Ticket - Clone (loss-policy=fence, standby, revoked)"
test_results
clean_empty

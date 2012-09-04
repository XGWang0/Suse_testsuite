#!/bin/bash
#Ticket - Clone (loss-policy=fence, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-9 "Ticket - Clone (loss-policy=fence, revoked)"
test_results
clean_empty

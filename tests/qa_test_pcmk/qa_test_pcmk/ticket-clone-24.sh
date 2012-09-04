#!/bin/bash
#Ticket - Clone (loss-policy=freeze, standby, revoked)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-24 "Ticket - Clone (loss-policy=freeze, standby, revoked)"
test_results
clean_empty

#!/bin/bash
#Ticket - Clone (loss-policy=freeze, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-23 "Ticket - Clone (loss-policy=freeze, granted, standby)"
test_results
clean_empty

#!/bin/bash
#Ticket - Clone (loss-policy=stop, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-14 "Ticket - Clone (loss-policy=stop, granted, standby)"
test_results
clean_empty

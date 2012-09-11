#!/bin/bash
#Ticket - Clone (loss-policy=fence, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-clone-20 "Ticket - Clone (loss-policy=fence, granted, standby)"
test_results
clean_empty

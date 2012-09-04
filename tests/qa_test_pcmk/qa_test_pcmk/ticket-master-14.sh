#!/bin/bash
#Ticket - Master (loss-policy=stop, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-14 "Ticket - Master (loss-policy=stop, granted, standby)"
test_results
clean_empty

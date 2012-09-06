#!/bin/bash
#Ticket - Master (loss-policy=fence, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-20 "Ticket - Master (loss-policy=fence, granted, standby)"
test_results
clean_empty

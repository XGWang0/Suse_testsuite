#!/bin/bash
#Ticket - Master (loss-policy=freeze, granted, standby)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test ticket-master-23 "Ticket - Master (loss-policy=freeze, granted, standby)"
test_results
clean_empty

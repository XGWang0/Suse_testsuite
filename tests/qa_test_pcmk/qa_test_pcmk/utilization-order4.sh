#!/bin/bash
#Utilization Order - Live Mirgration (bnc695440)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test utilization-order4 "Utilization Order - Live Mirgration (bnc695440)"
test_results
clean_empty

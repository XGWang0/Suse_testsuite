#!/bin/bash
#Order (mandatory keyword)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test order-mandatory "Order (mandatory keyword)"
test_results
clean_empty

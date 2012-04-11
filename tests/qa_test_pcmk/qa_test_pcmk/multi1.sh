#!/bin/bash
#Multiple Active (stop/start)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test multi1 "Multiple Active (stop/start)"
test_results
clean_empty

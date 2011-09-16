#!/bin/bash
#Don't shuffle master/slave instances unnecessarily
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-lf-1852 "Don't shuffle master/slave instances unnecessarily"
test_results
clean_empty

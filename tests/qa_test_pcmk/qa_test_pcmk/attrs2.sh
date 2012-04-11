#!/bin/bash
#string: lt / gt (and)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test attrs2 "string: lt / gt (and)"
test_results
clean_empty

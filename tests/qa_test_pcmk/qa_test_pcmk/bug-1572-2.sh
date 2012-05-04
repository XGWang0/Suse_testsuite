#!/bin/bash
#Recovery of groups depending on master/slave when the master is never re-promoted
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1572-2 "Recovery of groups depending on master/slave when the master is never re-promoted"
test_results
clean_empty

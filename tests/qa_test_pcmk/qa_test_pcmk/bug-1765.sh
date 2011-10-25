#!/bin/bash


#Master-Master Colocation (dont stop the slaves)
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-1765 "Master-Master Colocation (dont stop the slaves)"
test_results
clean_empty


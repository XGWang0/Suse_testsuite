#!/bin/bash
#Merge failcounts for anonymous clones
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-anon-failcount "Merge failcounts for anonymous clones"
test_results
clean_empty

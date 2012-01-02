#!/bin/bash


#Stable master placement
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test novell-239087 "Stable master placement"
test_results
clean_empty


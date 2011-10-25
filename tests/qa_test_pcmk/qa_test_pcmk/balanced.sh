#!/bin/bash


#Placement Strategy - balanced
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test balanced    "Placement Strategy - balanced"
test_results
clean_empty


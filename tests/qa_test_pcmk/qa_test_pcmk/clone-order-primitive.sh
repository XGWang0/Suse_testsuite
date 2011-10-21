#!/bin/bash


#Order clone start after a primitive
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test clone-order-primitive "Order clone start after a primitive"
test_results
clean_empty


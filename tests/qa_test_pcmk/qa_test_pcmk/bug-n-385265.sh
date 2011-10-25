#!/bin/bash


#Don't ignore the failure stickiness of group children - resource_idvscommon should stay stopped
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test bug-n-385265 "Don't ignore the failure stickiness of group children - resource_idvscommon should stay stopped"
test_results
clean_empty


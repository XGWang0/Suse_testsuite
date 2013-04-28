#/bin/bash

cd /usr/share/qa/qa_test_lynis
./prepare_for_suse.sh
./lynis -c --no-colors -Q


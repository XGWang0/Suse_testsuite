#!/bin/bash
#Don't displace prmExPostgreSQLDB2 on act2, Start prmExPostgreSQLDB1 on act3
. /usr/share/qa/qa_test_pcmk/regression.core.sh
do_test utilization-shuffle "Don't displace prmExPostgreSQLDB2 on act2, Start prmExPostgreSQLDB1 on act3"
test_results
clean_empty

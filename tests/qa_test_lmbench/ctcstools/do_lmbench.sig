#!/bin/bash
cd /usr/share/qa/qa_test_lmbench/results
if [ -d *linux-gnu ] ; then rm -r *linux-gnu ; fi
cd /usr/share/qa/qa_test_lmbench/src
#make rerun; make rerun; make rerun;
make clobber
make rerun_sig
cd /usr/share/qa/qa_test_lmbench/results
#find . -type d -maxdepth 1 | while read dirname;do
#  case ${dirname} in
#      *linux-gnu)
#         echo "Find Dir ${dirname}";;
#      *) continue
#  esac
#      cat ${dirname}/$(hostname).*
#done
make 

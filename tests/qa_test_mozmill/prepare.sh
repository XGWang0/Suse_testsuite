#!/bin/bash

pyver=$(python --version 2>&1 | awk '{print $2}' | awk -F"." '{print $1"."$2}')

if [ -e /usr/lib64/python$pyver/site-packages/ ]; then
	python_site=/usr/lib64/python2.6/site-packages
else
	python_site=/usr/lib/python$pyver/site-packages
fi

for i in ManifestDestiny-0.2.3.tar.gz mozrunner-2.5.3.tar.gz jsbridge-2.4.2.tar.gz mozmill-1.5.2.tar.gz; do
	easy_install -d $python_site /usr/share/qa/qa_test_mozmill/$i
done
ln -s $python_site/mozmill /usr/local/bin/
rm -f /usr/share/qa/qa_test_mozmill/*.tar.gz

tcffile=/usr/share/qa/qa_test_mozmill/tcf/qa_mozmill.tcf
casedir=/usr/share/qa/qa_test_mozmill/mozmillcases/firefox/
for i in `find $casedir *.js 2>/dev/null | egrep 'js$'`; 
do 
	casename=`echo $i | awk -F'/' '{print $NF}' | cut -d"." -f1`
	echo "timer 300" >> $tcffile
	echo "fg 1 $casename mozmill -t $i" >> $tcffile
	echo "wait" >> $tcffile
	echo >> $tcffile
done

ln -s /usr/share/qa/qa_test_mozmill/tcf/qa_mozmill.tcf /usr/share/qa/tcf/qa_mozmill.tcf
ln -s /usr/share/qa/qa_test_mozmill/test_mozmill-ctcs2-run /usr/share/qa/tools/test_mozmill-run
echo "MozMill tools were installed in $python_site"

# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#

echo > ../tcf/qa_pcmk.tcf
FILE=`mktemp /tmp/file.XXXX`
cat ./regression.sh | grep -v "#" | grep "do_test" > $FILE
while read line;do
	NAME=$(echo $line|awk '{print $2}')
	DESCRIPTION=$(echo $line|awk -F '"' '{print $2}')
	echo "#!/bin/bash" > ../$NAME.sh
	echo "#$DESCRIPTION" >> ../$NAME.sh
	echo ". /usr/share/qa/qa_test_pcmk/regression.core.sh" >> ../$NAME.sh
	echo "$line" >> ../$NAME.sh
	echo "test_results" >> ../$NAME.sh
	echo "clean_empty" >> ../$NAME.sh
	chmod +x ../$NAME.sh

	echo "fg 1 $NAME /usr/share/qa/qa_test_pcmk/$NAME.sh" >> ../tcf/qa_pcmk.tcf
	echo "wait" >> ../tcf/qa_pcmk.tcf
	echo -e "\n" >> ../tcf/qa_pcmk.tcf
done < $FILE
rm -f $FILE

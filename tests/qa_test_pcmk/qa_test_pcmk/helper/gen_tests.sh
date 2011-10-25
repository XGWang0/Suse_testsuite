

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

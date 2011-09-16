#!/bin/bash

source libqainternal.lib.sh

TESTUSER=testmail01
TESTALIAS=testmail01_alias
RESULT=$PASSED
CONFIG="conf/0010.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
ALIASES="conf/0010.aliases"
ORIGINAL_ALIASES="/etc/aliases"

ORIGINAL_ALIASES2="/tmp/aliases2"
COPY_FILE01="/tmp/copy01"
COPY_FILE02="/tmp/copy02"
COPY_FILE03="/tmp/copy03"
COPY_FILE04="/tmp/copy04"
TESTALIAS_FILE="file_alias"
TESTALIAS_PIPE="pipe_alias"
TESTALIAS_INCLUDE="include_alias"

SPOOLDIR="/var/spool/mail"

trap "cleanup" 0

function init() {
    if ! addUser "$TESTUSER"; then
        printMessage $MSG_ERROR "Unable to create user"
        exit $FAILED
    fi

    if ! copyConfig $CONFIG $ORIGINAL_CONFIG; then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! copyConfig $ALIASES $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
        exit $FAILED
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
        exit $FAILED
    fi

    if ! newaliases; then
        printMessage $MSG_ERROR "Unable to execute newaliases"
        exit $FAILED
    fi


}

function cleanup() {
    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    if ! removeConfig $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! newaliases; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    printMessage $MSG_INFO "Test #1: postalias(1) -s functionality"
    local tmp_result=$PASSED
    
    for i in "$TESTALIAS_FILE"  "$TESTALIAS_PIPE" "$TESTALIAS_INCLUDE" "$TESTALIAS"; do
        postalias -s "$ORIGINAL_ALIASES" | grep "$i" > /dev/null || tmp_result=$FAILED
    done

    if [ "$tmp_result" = "$PASSED" ]; then
        printMessage $MSG_PASSED "postalias -s test"
    else
        printMessage $MSG_FAILED "postalias -s test"
    fi
    return $tmp_result
}

function test02() {
    printMessage $MSG_INFO "Test #2: postalias(1) -q functionality"

    if ! postalias -q "$TESTALIAS_FILE" "$ORIGINAL_ALIASES" | 
          grep $COPY_FILE01 | grep $COPY_FILE02 > /dev/null; then
         
        printMessage $MSG_FAILED "postalias -q test"
        return $FAILED
    fi

    if ! postalias -q "$TESTALIAS_PIPE" "$ORIGINAL_ALIASES" | 
          grep 'cat' | grep $COPY_FILE03 > /dev/null; then
        
        printMessage $MSG_FAILED "postalias -q test"
        return $FAILED
    fi

    if ! postalias -q "$TESTALIAS_INCLUDE" "$ORIGINAL_ALIASES" | 
          grep "$ORIGINAL_ALIASES2" > /dev/null; then
          
        printMessage $MSG_FAILED "postalias -q test"
        return $FAILED
    fi

    #test for some non-existent key
    if postalias -q "THIS_ALIAS_DOES_NOT_EXISTS" "$ORIGINAL_ALIASES" > /dev/null; then
        printMessage $MSG_FAILED "postalias -q test"
        return $FAILED
    fi

    printMessage $MSG_PASSED "postalias -q test"
    return $PASSED
}


function test03() {
    printMessage $MSG_INFO "Test #3: postalias(1) -f functionality"

    #test the -f
    if postalias -f -q `echo $TESTALIAS_FILE | tr [a-z] [A-Z]` "$ORIGINAL_ALIASES" > /dev/null; then
        printMessage $MSG_FAILED "postalias -f test"
        return $FAILED
    fi
   
    printMessage $MSG_PASSED "postalias -f test"
    return $PASSED
}


function test04() {
    printMessage $MSG_INFO "Test #4: postalias(1) -d functionality"

    #test -d
    if ! postalias -d $TESTALIAS_FILE $ORIGINAL_ALIASES > /dev/null; then
        printMessage $MSG_FAILED "postalias -d test"
        return $FAILED
    fi
    
    #the alias is already deleted
    if postalias -d $TESTALIAS_FILE $ORIGINAL_ALIASES > /dev/null; then
        printMessage $MSG_FAILED "postalias -d test"
        return $FAILED
    fi

    #try to delete some non-existent key
    if postalias -d "THIS_ALIAS_DOES_NOT_EXISTS" "$ORIGINAL_ALIASES" > /dev/null; then
        printMessage $MSG_FAILED "postalias -d test"
        return $FAILED
    fi

    printMessage $MSG_PASSED "postalias -d test"
    return $PASSED
}

function test05() {
    printMessage $MSG_INFO "Test #5: postalias(1) -i functionality"

    #create new alias 
    if ! echo 'my_alias: hello_world' | postalias -i $ORIGINAL_ALIASES > /dev/null; then
        printMessage $MSG_FAILED "postalias -i test"
        return $FAILED
    fi

    #check the new alias
    if ! postalias -q "my_alias" $ORIGINAL_ALIASES | grep 'hello_world' > /dev/null; then
        printMessage $MSG_FAILED "postalias -i test"
        return $FAILED
    fi

    #delete the new alias
    if ! postalias -d "my_alias" $ORIGINAL_ALIASES > /dev/null; then
        printMessage $MSG_FAILED "postalias -i test"
        return $FAILED
    fi

    #query for some alias that should exist (e.i. nothing should get screwed)
    if ! postalias -q "$TESTALIAS_PIPE" "$ORIGINAL_ALIASES" | 
          grep 'cat' | grep $COPY_FILE03 > /dev/null; then
 
        printMessage $MSG_FAILED "postalias -i test"
        return $FAILED
    fi

    #query the deleted alias. It should be properly dismissed.
    if postalias -q "my_alias" $ORIGINAL_ALIASES | grep 'hello_world' > /dev/null; then
        printMessage $MSG_FAILED "postalias -i test"
        return $FAILED
    fi

    #try to add already existing alias
    #we expect that the alias name (key) will be part of the warning 
    # (in this case postalias returns 0)
    if ! echo "$TESTALIAS_PIPE: hello_world" | 
          postalias -i $ORIGINAL_ALIASES  2>&1 | grep "$TESTALIAS_PIPE" > /dev/null; then
          
        printMessage $MSG_FAILED "postalias -i test (adding existing alias)"
        return $FAILED
    fi

    #query the alias so we are sure it really wasn't added
    if postalias -q "$TESTALIAS_PIPE" $ORIGINAL_ALIASES | grep 'hello_world' ; then
        printMessage $MSG_FAILED "postalias -i test (querying existing alias)"
        return $FAILED
    fi

   
    printMessage $MSG_PASSED "postalias -i test"
    return $PASSED
}

function test06() {
    printMessage $MSG_INFO "Test #6: postalias(1) -irw functionality"

    #try to add already existing alias
    # we expect no output
    if echo "$TESTALIAS_PIPE: hello_world" | 
          postalias -iw $ORIGINAL_ALIASES  2>&1 | grep "$TESTALIAS_PIPE" > /dev/null; then
          
        printMessage $MSG_FAILED "postalias -iw test (adding existing alias)"
        return $FAILED
    fi

    #query the alias so we are sure it really wasn't added
    if postalias -q "$TESTALIAS_PIPE" $ORIGINAL_ALIASES | grep 'hello_world' ; then
        printMessage $MSG_FAILED "postalias -iw test (querying existing alias)"
        return $FAILED
    fi

    #try to add already existing alias + force
    if ! echo "$TESTALIAS_PIPE: hello_world" | 
          postalias -ir $ORIGINAL_ALIASES > /dev/null; then
          
        printMessage $MSG_FAILED "postalias -ir test (adding existing alias)"
        return $FAILED
    fi

    #query the alias so we are sure it really wasn't added
    if ! postalias -q "$TESTALIAS_PIPE" $ORIGINAL_ALIASES | grep 'hello_world' > /dev/null; then
        printMessage $MSG_FAILED "postalias -ir test (querying existing alias)"
        return $FAILED
    fi

    printMessage $MSG_PASSED "postalias -irw test"
    return $PASSED
}





init
test01 || RESULT=$?
test02 || RESULT=$?
test03 || RESULT=$?
test04 || RESULT=$?
test05 || RESULT=$?
test06 || RESULT=$?

exit $RESULT

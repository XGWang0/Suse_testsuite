#!/bin/bash

# See if 0 and 1 are not equal
if [ 0 == 1 ]
then
	echo "0 should not be greater than 1!"
	exit 22
fi

# See if a and a are equal
if [ "a" == "a" ]
then
	echo "a is a"
	exit 0
else
	exit 1
fi


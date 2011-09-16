#!/bin/bash

dirName=thisdir

# Make sure we are on i*86 (I know, this makes no sense, but it is only for demo purposes)
if [[ ! `arch` =~ i*86 ]]
then
	echo "You are not running i*86, so skipping this test." >&2
	exit 22
fi

# See if /$dirName doesn't yet exist
if [ -d /$dirName ]
then
	echo "Oops! /$dirName already was there. No idea what to do now. Bye!" >&2
	exit 11
fi

# Create /$dirName
mkdir /$dirName

# Now make sure /$dirName exists
if [ -d /$dirName ]
then
	echo "Yes! /$dirName was successfully created!"
	exit 0
else
	echo "Oops! /$dirName could not be created. That is unfortunate. Perhaps either you are not root, or your file system is really messed up. Bye!" >&2
	exit 1
fi

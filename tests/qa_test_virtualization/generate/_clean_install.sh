#!/bin/bash

#dir="$1"
#[ -d "$dir" ] && cd "$dir"

echo Warning: This will delete following files:
echo ==========================================
ls install_* 2> /dev/null | sed 's/^/  * /'
echo ==========================================
echo "Are you sure? (yes/no)"
read answer
[ "$answer" == "yes" ] && rm install_*


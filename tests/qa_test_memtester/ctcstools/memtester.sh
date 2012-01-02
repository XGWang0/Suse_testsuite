#!/bin/bash

BINFILE="/usr/bin/memtester"
MEMINFO="/proc/meminfo"

FREEMEM="$(grep LowFree $MEMINFO | tr -cd [:digit:])"
if test -z "$FREEMEM"; then
 FREEMEM="$(grep MemFree $MEMINFO | tr -cd [:digit:])"
fi
FREEMEM="$[FREEMEM-(FREEMEM/20)]" #leave some rem. mem free
FREEMEM="$[FREEMEM/1024]" #convert in MBytes

echo "Memtester.sh: Using $FREEMEM MBytes for test"
$BINFILE $FREEMEM $@



#!/bin/bash
set -eu

gcc zswap-test.c -o zswap-test


echo "Disable Zswap"
echo 0 > /sys/module/zswap/parameters/enabled
for m in 10000 20000 30000 31000 32000 33000 50000
do
./zswap-test $m
done

echo "Enable Zswap"
echo 1 > /sys/module/zswap/parameters/enabled
for m in 10000 20000 30000 31000 32000 33000 50000
do
./zswap-test $m
done

# This are upstreams tests for gzip, already integrated in slenkins gzip suites.

###cat helin-segv.sh
```
#!/bin/bash -x
# Before gzip-1.4, gzip -d would segfault on some inputs.

printf '\037\235\220\0\0\0\304' > helin.gz || exit 1
printf '\0\0' > exp || exit 1

fail=0

gzip -dc helin.gz > out || fail=1
cmp exp out || fail=1

exit $fail
```

## cat keep.sh
```
#!/bin/bash -x
# Exercise the --keep option.


echo fooooooooo > in || exit 1
cp in orig || exit 1

fail=0

# Compress and decompress both with and without --keep.
for k in --keep ''; do
  # With --keep, the source must be retained, otherwise, it must be removed.
  case $k in --keep) op='||' ;; *) op='&&' ;; esac

  gzip $k in || fail=1
  eval "test -f in $op fail=1"
  test -f in.gz || fail=1
  rm -f in || fail=1

  gzip -d $k in.gz || fail=1
  eval "test -f in.gz $op fail=1"
  test -f in || fail=1
  cmp in orig || fail=1
  rm -f in.gz || fail=1
done

exit $fail
```

cat memcpy-abuse.sh

```
#!/bin/bash -x 
# Before gzip-1.4, this the use of memcpy in inflate_codes could
# mistakenly operate on overlapping regions.  Exercise that code.

# less uniform than e.g., all zeros.
printf wxy%032767d 0 | tee in | gzip > in.gz || exit

fail=0

# Before the fix, this would call memcpy with overlapping regions.
gzip -dc in.gz > out || fail=1

cmp in out || fail=1

exit $fail
```
## cat mixed
```
#!/bin/bash 
# don't use bash -x in this test !

# Ensure that gzip -cdf handles mixed compressed/not-compressed data
# Before gzip-1.5, it would produce invalid output.


printf 'xxx\nyyy\n'      > exp2 || exit 1
printf 'aaa\nbbb\nccc\n' > exp3 || exit 1

fail=0

(echo xxx; echo yyy) > in || fail=1
gzip -cdf < in > out || fail=1
cmp exp2 out || fail=1

# Uncompressed input, followed by compressed data.
# Currently fails, so skip it.
# (echo xxx; echo yyy|gzip) > in || fail=1
# gzip -cdf < in > out || fail=1
# compare exp2 out || fail=1

# Compressed input, followed by regular (not-compressed) data.
(echo xxx|gzip; echo yyy) > in || fail=1
gzip -cdf < in > out || fail=1
cmp exp2 out || fail=1

(echo xxx|gzip; echo yyy|gzip) > in || fail=1
gzip -cdf < in > out || fail=1
cmp exp2 out || fail=1

in_str=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-+=%
for i in 0 1 2 3 4 5 6 7 8 9 a; do in_str="$in_str$in_str" ;done

# Start with some small sizes.  $(seq 64)
sizes=$(i=0; while :; do echo $i; test $i = 64 && break; i=$(expr $i + 1); done)

# gzip's internal buffer size is 32KiB + 64 bytes:
sizes="$sizes 32831 32832 32833"

# 128KiB, +/- 1
sizes="$sizes 131071 131072 131073"

# Ensure that "gzip -cdf" acts like cat, for a range of small input files.
i=0
for i in $sizes; do
  printf %$i.${i}s $in_str > in
  gzip -cdf < in > out
  cmp in out || fail=1
done
````

and other contained on the gzip.package /tests directory.

if you are interested on that, update the testsuite. ( i suggest it. ) i cannot do it because i don't know well ctf and i have no time for that.

cheers !



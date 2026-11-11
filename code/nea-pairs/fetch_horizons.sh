#!/bin/bash
# usage: hz_fetch.sh OUTDIR "designation" ...
out="$1"; shift
for des in "$@"; do
  f="$out/$(echo "$des" | tr ' ' '_').txt"
  [ -s "$f" ] && continue
  /usr/bin/curl -sS -m 300 -G "https://ssd.jpl.nasa.gov/api/horizons.api" \
    --data-urlencode "format=text" --data-urlencode "COMMAND='DES=$des;'" \
    --data-urlencode "EPHEM_TYPE=VECTORS" --data-urlencode "CENTER='500@10'" \
    --data-urlencode "START_TIME='1700-01-01'" --data-urlencode "STOP_TIME='2027-01-01'" \
    --data-urlencode "STEP_SIZE='2d'" --data-urlencode "VEC_TABLE='2'" \
    --data-urlencode "CSV_FORMAT=YES" --data-urlencode "OBJ_DATA=NO" -o "$f"
  echo "$des $(grep -c 'A.D.' "$f")"
done

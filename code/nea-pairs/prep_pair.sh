#!/bin/bash
# usage: prep_pair.sh OUTDIR "primary designation" "secondary designation"
# Fetches SBDB covariance for the secondary and Horizons states at its covariance epoch.
set -euo pipefail
out="$1"; A="$2"; B="$3"; mkdir -p "$out"
cmd(){ if [[ "$1" =~ ^[0-9]+$ ]]; then echo "$1;"; else echo "DES=$1;"; fi; }
sb(){ /usr/bin/curl -sS -m 60 -G "https://ssd-api.jpl.nasa.gov/sbdb.api" --data-urlencode "des=$1" --data-urlencode "cov=mat" --data-urlencode "full-prec=true" -o "$2"; }
sb "$A" "$out/sbdb_A.json"; sb "$B" "$out/sbdb_B.json"
epoch=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['orbit']['covariance']['epoch'])" "$out/sbdb_B.json")
echo "$epoch" > "$out/epoch.txt"
hz(){ /usr/bin/curl -sS -m 120 -G "https://ssd.jpl.nasa.gov/api/horizons.api" --data-urlencode "format=text" --data-urlencode "COMMAND='$1'" --data-urlencode "EPHEM_TYPE=$2" --data-urlencode "CENTER='$3'" --data-urlencode "TLIST='$epoch'" --data-urlencode "TLIST_TYPE=JD" --data-urlencode "TIME_TYPE=TDB" --data-urlencode "VEC_TABLE='2'" --data-urlencode "OUT_UNITS='AU-D'" --data-urlencode "REF_PLANE=ECLIPTIC" --data-urlencode "CSV_FORMAT=YES" --data-urlencode "OBJ_DATA=NO" -o "$4"; grep -q '\$\$SOE' "$4" || { echo "Horizons failed for $1"; exit 1; }; }
hz "$(cmd "$A")" ELEMENTS "500@10" "$out/el_A.txt"; hz "$(cmd "$B")" ELEMENTS "500@10" "$out/el_B.txt"
hz "$(cmd "$A")" VECTORS "500@0" "$out/v_A.txt"; hz "$(cmd "$B")" VECTORS "500@0" "$out/v_B.txt"
for b in 10 199 299 399 301 4 5 6 7 8; do hz "$b" VECTORS "500@0" "$out/v_$b.txt"; done
echo "$A / $B epoch $epoch ok"

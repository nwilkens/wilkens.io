# Near-Earth asteroid pair search

Scripts behind [A Candidate Asteroid Pair: 2018 NC15 and 2026 LD1](https://wilkens.io/research/nea-pair-2018-nc15-2026-ld1/).

Requires Python 3.12 with `numpy`, `pandas`, `scipy`, `matplotlib`, and `rebound`. Each script takes its data directory as an argument.

| Script | Input | Purpose |
|---|---|---|
| `load_catalog.py` | `sbdb_query.api` and `cad.api` JSON from ssd-api.jpl.nasa.gov | Parse the NEO catalog |
| `find_pairs.py` | Parsed catalog | Southworth-Hawkins search and randomized baseline |
| `along_track.py` | `sbdb_query.api` JSON with epochs and uncertainties | Mean-anomaly offset within each pair |
| `fetch_horizons.sh`, `separation_history.py` | JPL Horizons vectors | Nominal separation over time |
| `same_night_obs.py` | Minor Planet Center `get-obs` JSON | Same-station, same-night observations |
| `prep_pair.sh` | Two designations | Fetch SBDB covariance and Horizons states for a pair |
| `clones.py`, `clones_common.py` | Output of `prep_pair.sh` | Backward integration of orbit clones against the primary |
| `fig_clones.py` | Output of `clones.py` | Figure in the article |
| `fig_flyby.py` | Horizons vectors and observer tables, 6-hour step | Animation of the 2026 pass |
| `fig_brightness.py` | Horizons observer table, MPC observations | Brightness chart |
| `linkage.py` | MPC observations, Horizons | Test whether two designations are one object (short gap) |
| `linkage_clones.py` | Output of `prep_pair.sh`, MPC observations | Same test across a multi-year gap, using clones |
| `itf_search.py` | Output of `prep_pair.sh`, MPC isolated tracklet file, `ObsCodes.html` | Search unlinked detections for an object |

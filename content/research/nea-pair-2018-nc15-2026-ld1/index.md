---
title: "A Candidate Asteroid Pair: 2018 NC15 and 2026 LD1"
date: "2026-11-11T12:00:00Z"
description: "A search of every known near-Earth asteroid orbit turns up two bodies travelling within about one Earth-Moon distance of each other. I could not find the pair in the literature. Here is the evidence and what is still unverified."
tags: ["Astronomy", "Near-Earth Asteroids", "Asteroid Pairs", "Open Data", "NASA"]
---

Two asteroids are circling the Sun together. They follow the same path, they
are about as far apart as the Earth and the Moon, and one is about half the
size of the other. The simplest explanation is that they used to be one rock.
I could not find any record of anyone pointing this out before.

<div class="explainer">
<div class="explainer-row">
<svg viewBox="0 0 200 130" role="img" aria-label="Diagram of the Sun, Earth's orbit, and a larger orbit with two dots close together on it.">
<circle cx="92" cy="68" r="34" fill="none" stroke="#a6a6a6" stroke-width="1"/>
<ellipse cx="108" cy="62" rx="56" ry="52" fill="none" stroke="#3987E5" stroke-width="1.5" opacity="0.8"/>
<circle cx="92" cy="68" r="5" fill="#e8c547"/>
<circle cx="126" cy="68" r="3.5" fill="#fafafa"/>
<circle cx="150" cy="96" r="4" fill="#3987E5"/><circle cx="143" cy="102" r="3" fill="#EF5F2E"/>
<text x="92" y="84" text-anchor="middle">Sun</text><text x="126" y="60" text-anchor="middle">Earth</text><text class="ink" x="160" y="118" text-anchor="middle">the pair</text>
</svg>
<div><h3>Two asteroids, one path</h3><p>2018 NC15 and 2026 LD1 follow the same orbit around the Sun, a little outside Earth's. One lap takes two years. They never come closer to Earth than about 18 million km.</p></div>
</div>
<div class="explainer-row">
<svg viewBox="0 0 200 130" role="img" aria-label="Two scale bars. Earth to Moon is 384,000 km. The gap between the two asteroids is 310,000 km.">
<line x1="15" y1="38" x2="185" y2="38" stroke="#a6a6a6" stroke-width="1" stroke-dasharray="3 3"/>
<circle cx="15" cy="38" r="7" fill="#fafafa"/><circle cx="185" cy="38" r="3" fill="#a6a6a6"/>
<text x="15" y="20" text-anchor="start">Earth</text><text x="185" y="20" text-anchor="end">Moon</text><text class="ink" x="100" y="58" text-anchor="middle">384,000 km</text>
<line x1="15" y1="96" x2="152" y2="96" stroke="#a6a6a6" stroke-width="1" stroke-dasharray="3 3"/>
<circle cx="15" cy="96" r="5" fill="#3987E5"/><circle cx="152" cy="96" r="3.5" fill="#EF5F2E"/>
<text x="15" y="80" text-anchor="start">2018 NC15</text><text x="152" y="80" text-anchor="end">2026 LD1</text><text class="ink" x="84" y="116" text-anchor="middle">310,000 km</text>
</svg>
<div><h3>Travelling side by side</h3><p>Asteroids that share an orbit by chance would be scattered around the Sun, hundreds of millions of km apart. These two are separated by less than the distance from the Earth to the Moon.</p></div>
</div>
<div class="explainer-row">
<svg viewBox="0 0 200 130" role="img" aria-label="Two circles, the second about half the width of the first.">
<circle cx="68" cy="58" r="40" fill="#3987E5" opacity="0.85"/><circle cx="152" cy="78" r="20" fill="#EF5F2E" opacity="0.9"/>
<text class="ink" x="68" y="118" text-anchor="middle">2018 NC15</text><text class="ink" x="152" y="118" text-anchor="middle">2026 LD1</text>
</svg>
<div><h3>Probably once a single rock</h3><p>The larger one is roughly 100 to 250 metres across, about the size of a stadium. The smaller is about half that. Small asteroids can spin fast enough to throw off a piece, which then drifts away at walking pace.</p></div>
</div>
</div>

Some care is needed with the numbers. The smaller asteroid was only discovered
in June 2026 and was tracked for 27 days, so its path is not known well
enough to say when the two separated. This is a candidate, not a confirmed
result, and it has not been peer reviewed.

The rest of this article is the evidence. It gets more technical as it goes.

## Summary

- 2018 NC15 was discovered in 2018 and has been tracked for eight years.
  2026 LD1 was discovered on 5 June 2026 and has a 27-day observation arc,
  meaning all measurements of it span 27 days.
- Their orbits match more closely than any other pair of distinct objects in
  the near-Earth asteroid catalog.
- The Catalina Sky Survey measured both objects in the same minute, on two
  nights, 1.25 degrees apart. They are two bodies, not one object entered
  twice.
- 2026 LD1 is about 1.5 magnitudes fainter (about four times dimmer), so it
  is roughly half the diameter of 2018 NC15.
- When they passed Earth in June 2026 they were about 500,000 km apart. As of
  November 2026 the gap is about 310,000 km.
- The date they separated cannot be determined yet.

## The June 2026 pass

<figure>
<video controls muted loop playsinline preload="metadata" poster="flyby-2026-poster.png" src="flyby-2026.mp4"></video>
<figcaption>April to August 2026, from JPL Horizons positions. Left: the shared orbit seen from above the Solar System; at this scale the two asteroids are a single dot. Right: where 2026 LD1 appeared in the sky relative to 2018 NC15, with north up and east to the left. The rings mark the two nights when the Catalina Sky Survey recorded both. The pair came no closer to Earth than 19.7 million km.</figcaption>
</figure>

## What an asteroid pair is

An asteroid pair is two asteroids on nearly identical orbits around the Sun
that are not bound to each other. The usual explanation is that they were
once one body. A small asteroid that spins fast enough can shed material, and
the fragment drifts away at walking speed. Pairs are common in the main belt.
Among near-Earth asteroids only a handful are known, because planetary
encounters scatter their orbits within a few thousand years.

## How the pair turned up

I downloaded the orbital elements of all 43,025 near-Earth asteroids from the
JPL Small-Body Database and compared every orbit with every other orbit using
the Southworth-Hawkins criterion, a standard distance measure between two
orbits. A value below about 0.01 is usually considered worth a look.

To see how many close matches chance alone would produce, I repeated the
search 20 times with each asteroid's orbit rotated by a random angle. That
keeps the distribution of orbit sizes, shapes, and tilts but breaks any real
association.

| Threshold | Pairs found | Pairs expected by chance |
|---|---|---|
| D < 0.003 | 12 | 0.0 |
| D < 0.005 | 14 | 0.5 |
| D < 0.010 | 32 | 6.6 |

The tightest matches are below. I left out four whose observation arcs are
ten days or less, where the two entries may be one object catalogued twice.

| Pair | D | Status |
|---|---|---|
| 2018 NC15 / 2026 LD1 | 0.0001 | Not found in the literature |
| 2012 QG8 / 2024 GE1 | 0.0003 | Reported by Liu et al., 2026 |
| 2019 PR2 / 2019 QR6 | 0.0004 | Reported by Fatka et al., 2022 |
| 2022 MY3 / 2022 OP8 | 0.0010 | Reported by Liu et al., 2026 |
| (357414) 2003 XE / 2023 YD2 | 0.0017 | Not found in the literature |
| 2024 SO3 / 2026 FO1 | 0.0023 | Not found in the literature |
| 2017 SN16 / 2018 RY7 | 0.0026 | Reported by Moskovitz et al., 2019 |
| 2015 EE7 / 2015 FP124 | 0.0028 | Reported by Moskovitz et al., 2019 |

Five of the eight are published pairs, which is a useful check that the
search works. Liu et al. published the same kind of search in August 2026.
2026 LD1 was discovered in June 2026, most likely after their catalog
snapshot.

## Evidence that this is a real pair

**They are two objects.** The Minor Planet Center's observation records show
the Catalina Sky Survey (station G96) measuring both asteroids at the same
time on 5 June 2026 and again on 21 June 2026.

| Date (UT) | Separation on the sky | Magnitude, 2018 NC15 | Magnitude, 2026 LD1 |
|---|---|---|---|
| 2026-06-05 05:32 | 1.25° | 19.7 | 21.3 |
| 2026-06-21 06:27 | 1.27° | 19.3 | 20.8 |

**They are close together in space.** JPL's integrated orbits put the two
about 500,000 km apart during the June 2026 pass. The gap changes as they go
around the orbit, between 265,000 and 520,000 km over 2026. The position of
2026 LD1 is uncertain by roughly 50,000 km. On the nominal orbits the gap has
been closing: it was 1.5 to 2.0 million km in 2018.

**Only the timing differs clearly.** Taken one at a time, each orbital element
of 2026 LD1 agrees with 2018 NC15 to within 0.4 standard deviations. The
exception is the time of perihelion: 2026 LD1 passes 0.18 days later, a
difference of 24 standard deviations. When the correlations between elements
are included, the orbit shapes do differ by a small but significant amount
(chi-squared of about 350 on 5 degrees of freedom). That is what a slow separation
would produce.

**Chance is not a plausible explanation.** The randomized catalogs produced no
pair this tight in 20 trials. That test does not even require the two objects
to be at the same point along the orbit, which these are.

## When did they separate?

The orbit of 2026 LD1 is known only within a margin of error. To see what
that margin allows, I drew 400 slightly different versions of its orbit
("clones") from the published uncertainty and integrated each one backward
500 years with the Sun, the eight planets, and the Moon. The chart shows how
far each clone was from 2018 NC15 over that time.

<figure>
<img src="clone-separation.png" alt="Line chart on a log scale. The median separation between 2018 NC15 and 400 clones of 2026 LD1 rises from about 300,000 km today to about 50 million km 500 years ago. Thirty-four clones pass within 10,000 km of 2018 NC15 at some point in that period, most of them around 400 years ago.">
<figcaption>Separation between 2018 NC15 and 400 clones of 2026 LD1 over the last 500 years. Most clones were farther away in the past. Thirty-four pass within 10,000 km.</figcaption>
</figure>

- About 83% of the clones were farther from 2018 NC15 throughout the last
  500 years than they are now. For those orbits the separation happened
  earlier, probably thousands of years ago.
- Ten clones (2.5%) pass within 3,000 km of 2018 NC15 between 74 and 465
  years ago. Nine of them do so at under 1 m/s, and the slowest at 0.07 m/s.
  That is the speed range expected when a small asteroid sheds a fragment.

Both outcomes fit the data. The separation date is not constrained.

## The same test on published pairs and other candidates

To see what this test shows for pairs that are already accepted, I ran it
unchanged on two pairs from Liu et al. and on the other close matches from my
search.

| Pair | Clones within 10,000 km | Of those, under 1 m/s | Slowest pass |
|---|---|---|---|
| 2018 NC15 / 2026 LD1 | 34 | 15 | 0.07 m/s |
| 2012 QG8 / 2024 GE1 (published) | 37 | 5 | 0.38 m/s |
| 2022 MY3 / 2022 OP8 (published) | 32 | 0 | 1.95 m/s |
| (357414) 2003 XE / 2023 YD2 | 0 | 0 | 21 m/s |
| 2024 SO3 / 2026 FO1 | 0 | 0 | none within 100,000 km |
| 2005 TF / 2024 WS19 | 0 | 0 | 98 m/s |
| (31346) 1998 PB1 / 2023 PV | 0 | 0 | none within 100,000 km |

Each row is 400 clones over 500 years. 2018 NC15 / 2026 LD1 behaves like the
two published pairs: a few percent of its possible orbits meet the larger
body closely and slowly. The other four do not. Their orbits look alike, but
in this test they never meet gently, so I no longer count them as candidates.
A separation older than 500 years is not ruled out for any of them.

## A way to settle it

2018 NC15 returns to Earth's neighborhood every two years. During the June
2024 return, 2026 LD1 should have been bright enough for the large surveys to
record, about two degrees from 2018 NC15.

| Date | Predicted magnitude | Distance from 2018 NC15 on the sky | Position uncertainty (3 sigma) |
|---|---|---|---|
| 2024-06-03 | 20.9 | 2.4° | 10° |
| 2024-06-18 | 20.3 | 2.2° | 9° |
| 2024-07-03 | 20.8 | 1.5° | 6° |

<figure>
<img src="brightness.png" alt="Line chart of predicted apparent magnitude for 2018 NC15 and 2026 LD1 from 2018 to 2026. Both brighten every two years. 2026 LD1 reaches magnitude 20.2 in June 2024, brighter than the approximate survey limit of 21.5, and was not detected then. Tick marks show the nights each object was observed.">
<figcaption>Predicted brightness of both asteroids at each return. 2026 LD1 was above the approximate survey limit only in 2024 and 2026. The tick marks along the bottom show the nights each object was actually observed.</figcaption>
</figure>

The uncertainty runs along the orbit track, so the search area is a line
rather than a circle. One detection would extend the arc of 2026 LD1 from 27
days to two years, which would shrink the uncertainty enough to compute a
separation date.

I have made two attempts so far.

- **Unlinked detections: nothing found.** The Minor Planet Center keeps a file
  of moving objects that surveys reported but nobody has matched to a known
  asteroid. I compared 22,557 of those from May to August 2024 against
  20,000 clones of 2026 LD1. None matched. The closest was 191 arcseconds
  off and moving in the wrong direction. The same code reproduces the 2026
  observations of 2026 LD1 to 0.4 arcseconds, so a real match would have
  stood out.
- **Survey images: they exist.** The Zwicky Transient Facility archive has 30
  public exposures from May and June 2024 that cover both 2018 NC15 and the
  predicted position of 2026 LD1. In the frames from 15 to 28 June the
  companion is predicted at magnitude 20.4 to 20.6, close to the limit of a
  single exposure. The Moon was full on 22 June 2024, which makes faint
  objects harder to detect and may be why no survey reported it. Adding the
  frames together along the predicted motion could still show it. I have not
  done that yet.

The next returns are worse. In June 2028 the companion peaks near magnitude
22.2, and in 2030 near 23.3. The 2024 images are the best data that will
exist for several years.

## Catalog entries that are one object

Four of the closest matches in the search turned out not to be pairs. In each
case two catalog entries describe a single asteroid.

| Entries | Finding | Evidence |
|---|---|---|
| 2026 SW11 and 2026 SA12 | Same object, entered twice | Each orbit predicts the other's observations to about 1 arcsecond |
| 2026 VO and 2026 VR1 | Same object, entered twice | Same test, 0.4 to 0.8 arcseconds |
| 2017 RB15 and 2026 RG39 | Very likely the same object on two returns, nine years apart | One of 6,000 clones of the 2026 orbit matches all six nights of 2017 observations to within 0.04 to 0.17 degrees |
| 2010 VL65 and 2021 UA12 | Probably the same object, eleven years apart | 55 of 6,000 clones match all five nights of 2010 observations to within 0.5 degrees |

The last two matter a little more than the first two. Each object has only
been tracked for about ten days at a time. Linking the two visits would give
each a multi-year orbit. My test for those two uses positions as seen from
the centre of the Earth, which is accurate to a few tenths of a degree for
objects this close, so they need a proper joint orbit fit to confirm.

## Limits

- The whole case rests on a 27-day arc for 2026 LD1. More observations could
  change its orbit.
- The clone integration leaves out the Yarkovsky thermal drift and general
  relativity. Both are much smaller than the orbit uncertainty over 500 years,
  but a proper age estimate needs them.
- I searched for prior reports of this pair and found none. A preprint or a
  Minor Planet Center note could exist that the search did not surface.
- The JPL database holds no size, spectrum, rotation period, or radar data
  for either object, and no infrared survey frames cover them. Matching
  composition would strengthen the case.

## Methods and data

- Orbital elements, uncertainties, and covariance: JPL Small-Body Database
  API, retrieved 11 November 2026.
- Positions over time: JPL Horizons.
- Observation records: Minor Planet Center observations API and isolated
  tracklet file, retrieved 11 November 2026.
- Archive image search: NASA/IPAC Infrared Science Archive moving-object
  search, Zwicky Transient Facility catalog.
- Orbit comparison: Southworth-Hawkins D criterion, with a k-d tree to find
  candidate neighbors.
- Clone integration: REBOUND with the IAS15 integrator.

The analysis was done with Claude Code. The scripts are in the
[site repository](https://github.com/nwilkens/wilkens.io/tree/main/code/nea-pairs).

## Changes

- 11 November 2026: corrected the separation during the June 2026 pass from
  320,000 km to about 500,000 km. Added the video and brightness chart.
- 11 November 2026: extended the clone test to 500 years, ran it on published
  pairs and the other candidates, resolved four double entries, and added
  the search of unlinked detections.

## References

- Liu, N., et al. (2026). Search for Near-Earth Asteroid
  Pair Candidates Based on Orbital Evolution Analysis. *The Astrophysical
  Journal*. [doi:10.3847/1538-4357/ae876e](https://doi.org/10.3847/1538-4357/ae876e)
- Fatka, P., et al. (2022). Recent formation and likely cometary activity of
  near-Earth asteroid pair 2019 PR2 and 2019 QR6.
  [arXiv:2112.01681](https://arxiv.org/abs/2112.01681)
- Moskovitz, N., et al. (2019). A common origin for dynamically associated
  near-Earth asteroid pairs.
  [arXiv:1905.12058](https://arxiv.org/abs/1905.12058)
- Minor Planet Center.
  [MPEC 2026-L56: 2026 LD1](https://www.minorplanetcenter.net/mpec/K26/K26L56.html)

---
title: "Asking Questions Outside My Field"
date: "2026-11-11T17:00:00Z"
description: "I am not an astronomer. In one working session with Claude I went from a vague question about NASA's open data to a candidate asteroid pair nobody seems to have reported. What made that possible, and what kept it honest."
tags: ["AI", "Research", "Claude", "Open Data", "Agentic Engineering"]
---

I build cloud infrastructure. I have never taken an astronomy course. This
week I published
[a candidate asteroid pair]({{< relref "research/nea-pair-2018-nc15-2026-ld1" >}}) that I
could not find in the scientific literature. This post is about how that
happened, because I think the how matters more than the asteroid.

## The question was vague

I started with one sentence: NASA publishes a lot of data, so pick a dataset
and look for something nobody has found. That is not a research question. It
is curiosity, and until recently curiosity in a field you do not know went
nowhere. You would need months to learn which datasets exist, what the
standard methods are, and what has already been done.

## What Claude did with it

Claude surveyed the catalog and reported that most of it was a poor fit:
36,000 entries, nearly all pointers to large archives that science teams
have already worked over. It picked two sources with fresh data and said why.

The first attempt, on space-weather forecasts, found nothing new. It
confirmed results that are already published. Claude said so plainly and
moved on.

The second attempt compared the orbit of every known near-Earth asteroid
with every other one. That is 43,000 objects and a standard method I had
never heard of. It turned up a handful of very close matches.

## What kept it honest

This is the part I would not skip.

- **It checked whether the result was already known.** Two of the top matches
  had been published three months earlier by a group doing the same kind of
  search. That was disappointing for about a minute. Then it was the best
  news of the day: an independent team had found the same things with the
  same method, so the method works. The tightest match of all was not in
  their paper, because the second asteroid was discovered after they
  finished.
- **It went to the raw observations.** The claim that these are two objects
  does not rest on a model. A telescope in Arizona recorded both in the same
  minute on two different nights.
- **It said what it could not show.** The article states that the age of the
  pair cannot be determined, and gives the reason.
- **It caught its own mistake.** While building a video of the pass, the
  numbers on screen disagreed with a figure in the article. The article was
  wrong. It was corrected the same hour and the correction is in the commit
  history.

## What I brought

Not expertise. I brought the question, a nudge to look at near-Earth objects
when the first idea came up dry, and the decisions: which finding to pursue,
whether to publish, how much to claim. I also brought suspicion. I read the
result as someone who expects to be wrong.

## What this changes

There are a lot of people like me. We know one field well and are curious
about others. The cost of acting on that curiosity used to be years. Now it
is an afternoon, provided you hold the result to the standard the field
would: check the literature, check the raw data, publish the code, and say
what is unverified.

I do not know yet whether this pair will hold up. The next step is to send
it to people who can tell me. Either way, I asked a question I had no
business asking, and I got an answer I can check.

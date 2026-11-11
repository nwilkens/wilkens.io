---
title: "Acquiring Triton DataCenter from Samsung"
date: "2024-08-20T00:00:00.000Z"
description: "What it takes to acquire an open-source infrastructure platform from a semiconductor giant, and what happens after you do."
tags: ["Open Source", "Acquisition", "Triton", "SmartOS", "Cloud"]
readingTime: 10
---

In May 2022, MNX.io completed the acquisition of the Triton DataCenter and SmartOS platforms from Samsung. This is the story of how that happened and what we learned.

  ## Background

  Joyent built Triton DataCenter — one of the most technically sophisticated cloud platforms ever built. Native container support before Docker existed. Hardware virtualization (bhyve, KVM) on illumos. Distributed object storage (Manta). Software-defined networking. The engineering was exceptional.

  Samsung acquired Joyent in 2016 for approximately $170M. By 2022, Samsung's priorities had shifted and they were looking to transition stewardship of the open-source platforms.

  ## Why MNX.io

  MNX.io had been running Triton in production since 2013. We were operators, not just users. We understood the platform at a deep level — the internals, the failure modes, the operational requirements. We had relationships in the Triton and SmartOS community.

  When Samsung was ready to find a new home for the platforms, we were a natural fit.

  ## The Negotiation

  I'm not going to go into deal specifics, but a few things stood out about negotiating with a major corporation for open-source stewardship:

  **Mission matters.** Samsung cared that the platform would be maintained and the community would be served. It wasn't purely financial. We had to demonstrate a credible path to continued development and community support.

  **Operational readiness.** We had to show we could actually run the platform — support enterprise customers, do release engineering, maintain the build infrastructure. A decade of running it in production was our strongest argument.

  **Technical depth.** The engineering discussions weren't high-level. We went deep on architecture, roadmap, and specific technical challenges. This was engineers evaluating engineers.

  ## After Acquisition

  Taking on stewardship of an open-source platform is different from acquiring a product company. The community is the product. If the community doesn't trust you, the platform dies.

  The first six months were mostly listening. Understanding what the community needed. Understanding what enterprise customers needed. Understanding where Samsung had made investments and where there were gaps.

  We then focused on:
  - Release cadence — consistent, reliable releases
  - Build infrastructure — modernizing and stabilizing the CI/CD pipeline
  - Enterprise support — making it viable for organizations to run Triton in production
  - Community governance — establishing clear processes for contributions and decision-making

  ## The Edgecast Acquisition

  Triton's orchestration capabilities and object storage economics turned out to be exactly what Edgecast needed for CDN delivery. That's what drove the acquisition of MNX.io by Edgecast in 2024.

  Sometimes the right technical foundation attracts the right acquirer.

---
title: "Context Engineering: The Skill That Actually Matters for LLM Applications"
date: "2025-06-01T00:00:00.000Z"
description: "Prompt engineering gets all the attention. Context engineering is where the real leverage is. Here's how to think about it."
tags: ["AI", "LLM", "RAG", "Engineering", "Context Engineering"]
readingTime: 8
---

Everyone talks about prompt engineering. The real skill for building useful LLM applications is context engineering.

  ## What's the Difference?

  **Prompt engineering** is about how you phrase requests to the model. Use chain-of-thought. Be specific. Give examples. Assign a role. These things matter, but they're table stakes.

  **Context engineering** is about what information you give the model to work with. What does it need to know to do the task well? How do you get that information to it efficiently? How do you manage context windows across a long conversation or multi-step task?

  In my experience building production AI systems, context engineering has 10x more leverage than prompt engineering.

  ## The Context Problem

  Language models are powerful but amnesiac. Each request starts fresh. They know what's in their training data and what's in the current context window. That's it.

  For most enterprise use cases, the limiting factor isn't model capability — it's context. The model doesn't know your codebase. It doesn't know your architecture decisions. It doesn't know your team's conventions. It doesn't know what happened in last week's incident.

  Give it that context, and its output quality improves dramatically.

  ## The Four Layers of Context

  I think about context in four layers:

  **1. Static Knowledge**
  Documentation, architecture references, runbooks, code standards. Things that change slowly. Best served via RAG — retrieve relevant chunks at query time rather than stuffing everything into every request.

  **2. Session Context**
  What's happened in the current conversation or task. Conversation history, intermediate results, decisions made so far. Managed by maintaining a structured context object that evolves as the task proceeds.

  **3. Environmental Context**
  Current state of the system — what code exists, what's deployed, what's running. Best served via tool calls that fetch live data rather than static snapshots.

  **4. Ephemeral Context**
  Task-specific information provided by the user. What they're trying to accomplish, constraints, preferences. Usually just what they said.

  ## Practical Techniques

  **Retrieval-Augmented Generation (RAG):** Build a retrieval system over your static knowledge. When a query arrives, retrieve the most relevant chunks and include them in context. Vector search works well for semantic similarity. Keyword search still wins for specific identifiers. Use both.

  **Structured Context Objects:** For multi-step agents, maintain a structured object that captures current state. Pass it explicitly to each LLM call. This is more reliable than relying on conversation history.

  **Tool-Based Context Retrieval:** Give the model tools to fetch context dynamically. "Look up the schema for this table." "Get the last 10 errors from this service." "Read this file." The model requests what it needs rather than you guessing what to include.

  **Context Compression:** For long contexts, use a smaller/cheaper model to summarize earlier parts of the conversation before passing to the main model. You lose some detail but stay within context limits.

  ## The Context Window Is Not Unlimited

  Even with large context windows, stuffing everything in is not the answer. Relevant context improves performance. Irrelevant context degrades it — the model has to work harder to find the signal in the noise.

  Be selective. Retrieve what's relevant, not everything that might be relevant.

  ## Where This Is Going

  The most sophisticated AI systems I've seen don't try to make the model smarter. They make the context richer. The model's job is reasoning and generation. The engineering team's job is making sure the model has what it needs to do that well.

  This is fundamentally an information retrieval and management problem dressed up as an AI problem. Engineers who understand how to build good retrieval systems — search, databases, caching, data pipelines — have a significant advantage here.

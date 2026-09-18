# EvoHarness Reading List

This file records the papers and repositories that are directly relevant to the current EvoHarness route.

The purpose is not to build a broad survey. Codex should use this list to understand which ideas are being adapted and which source repositories should be inspected before implementation.

---

## 1. AppWorld

**Paper**

AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents

- Venue: ACL 2024
- Role in EvoHarness: primary benchmark and execution environment
- Paper: https://aclanthology.org/2024.acl-long.850/
- Official repository: https://github.com/StonyBrookNLP/appworld
- Local source:
  - `G:\harness\third_party\appworld`

### What to read

Focus on:

- simplified function-calling agent
- agent loop
- message / trajectory representation
- tool-call representation
- tool observations
- task initialization
- task completion
- evaluator
- experiment configuration

### Why it matters

AppWorld provides a controllable environment with state-based evaluation for long-horizon API/tool-use tasks. EvoHarness should preserve AppWorld's benchmark semantics and modify only the agent harness around the frozen LLM.

---

## 2. ACON

**Paper**

ACON: Optimizing Context Compression for Long-horizon LLM Agents

- Venue: ICML 2026
- arXiv: https://arxiv.org/abs/2510.00615
- Official repository: https://github.com/microsoft/acon
- Local source:
  - `G:\harness\third_party\acon`

### Main idea

ACON optimizes context compression for long-horizon agents.

It operates on two important sources of context growth:

- environment observations
- interaction history

A key idea is to use failures where full context succeeds but compressed context fails to diagnose what information compression removed incorrectly. These failures are then used to improve the natural-language compression guideline.

### What EvoHarness should borrow

Prioritize:

- AppWorld integration
- context/history interception points
- compressor interface
- compressed-state representation
- compression guideline optimization
- failure analysis for information loss
- peak context / token metrics

Do not prioritize:

- compressor distillation
- LoRA
- agent distillation
- any model-weight training stage

### EvoHarness adaptation

ACON is the main reference for **within-task context optimization**.

EvoHarness should first reproduce a clean full-history baseline, then implement context optimization as an explicit harness component.

---

## 3. ACE

**Paper**

Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

- Venue: ICLR 2026
- Official publication page:
  - https://www.microsoft.com/en-us/research/publication/agentic-context-engineering-evolving-contexts-for-self-improving-language-models/
- ICLR page:
  - https://iclr.cc/virtual/2026/poster/10008343

### Main idea

ACE treats context as an evolving playbook rather than a static prompt or repeatedly rewritten summary.

Its core loop uses:

- Generator
- Reflector
- Curator

The playbook evolves through structured incremental updates rather than full rewrites.

Typical operations conceptually include:

- ADD
- UPDATE
- REMOVE

The goal is to preserve useful detail while avoiding context collapse and brevity bias.

### What EvoHarness should borrow

Use ACE mainly for **cross-task experience accumulation**:

- structured experience items
- incremental updates
- success/failure reflection
- playbook curation
- avoiding complete memory rewrites
- preserving reusable procedural knowledge

Do not implement ACE during the first milestone.

The context baseline and V1 must work first.

---

## 4. ReasoningBank

**Paper**

ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory

- Venue: ICLR 2026
- OpenReview:
  - https://openreview.net/forum?id=jL7fwchScm
- Official repository:
  - https://github.com/google-research/reasoning-bank
- Google Research overview:
  - https://www.research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/

### Main idea

ReasoningBank learns reusable reasoning memory from both:

- successful trajectories
- failed trajectories

It stores generalizable reasoning strategies rather than simply replaying raw traces.

### What EvoHarness should borrow

Use ReasoningBank as a complementary reference for the Experience Playbook:

- learn from failures, not only successes
- distill strategies instead of storing entire trajectories
- retrieve relevant experience on future tasks
- separate raw trajectory storage from reusable reasoning memory

### EvoHarness adaptation

The intended EvoHarness memory should combine:

- ACE-style incremental curation
- ReasoningBank-style strategy extraction from success and failure

The result should be a structured **Experience Playbook**, not a raw vector database of trajectories.

---

## 5. GEPA

**Paper**

GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

- Venue: ICLR 2026
- ICLR paper:
  - https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html
- Official repository:
  - https://github.com/gepa-ai/gepa

### Main idea

GEPA performs reflective optimization in natural-language/text space.

It uses execution traces and evaluation feedback to:

- diagnose failures
- propose targeted textual changes
- evaluate candidates
- retain useful variants
- maintain diversity through Pareto-aware selection

### What EvoHarness should borrow

Use GEPA only at the outer harness-optimization stage.

Potential optimization targets:

- system prompt
- tool-use policy
- context-compression guideline
- memory retrieval instruction
- error recovery rule
- stopping rule

### Important scope restriction

EvoHarness does **not** use GEPA as a reason to add GRPO, PPO, RL fine-tuning, or model-weight updates.

The relevant idea is reflective text/harness evolution.

Do not implement this during the first milestone.

---

# Project Synthesis

The current EvoHarness route combines the papers at different time scales.

```text
Within one task
    |
    +-- ACON
    |   context / observation compression
    |
Across tasks
    |
    +-- ACE
    |   incremental evolving playbook
    |
    +-- ReasoningBank
    |   reasoning strategies from success + failure
    |
Across a batch of trajectories
    |
    +-- GEPA
        reflective harness optimization
```

The goal is not to reproduce every paper completely.

The goal is to reuse the parts that answer one coherent research question:

> Can a frozen LLM become a better long-horizon tool agent through systematic optimization of the harness around it?

---

# Planned Original Integration

The current planned integration mechanism is:

## Failure-Routed Harness Adaptation

After a failed task:

1. inspect the trajectory and evaluator result
2. classify the likely failure source
3. route the failure to the relevant harness component
4. update only that component
5. validate the new variant

Possible routes:

```text
missing information after compression
    -> context/compressor

missing reusable strategy
    -> experience playbook

bad tool-use or recovery behavior
    -> harness instruction

premature stop / repeated action
    -> loop policy
```

This mechanism is intended to connect ACON, ACE/ReasoningBank, and GEPA without blindly updating every component after every task.

---

# Reading Order for Codex

When starting implementation work, inspect material in this order:

1. AppWorld simplified function-calling agent
2. AppWorld evaluator and task lifecycle
3. ACON AppWorld integration
4. ACON context compressor and guideline optimization
5. Only later: ACE
6. Only later: ReasoningBank
7. Only later: GEPA

Do not jump directly to memory or harness evolution before the V0 baseline and V1 context experiments work.

---

# Current Milestone

The current milestone requires only:

- AppWorld
- ACON
- EvoHarness

ACE, ReasoningBank, and GEPA are reading references for later stages.

They do not need to be cloned or installed yet.

# EvoHarness Project Plan

## 1. Project Positioning

EvoHarness is a research project for improving long-horizon tool-using LLM agents through harness-level optimization.

The base LLM remains frozen.

The project does **not** use:

- GRPO
- PPO
- SFT
- RL fine-tuning
- model-weight updates
- Docker as a required runtime dependency

The project focuses on the system surrounding the model:

- active context
- tool observations
- trajectory representation
- cross-task experience
- failure analysis
- harness instructions
- evaluation

---

## 2. Main Benchmark

Primary benchmark:

- AppWorld

Primary reference agent:

- AppWorld simplified function-calling agent

Reference source:

- `G:\harness\third_party\appworld`

The local Windows machine is mainly used for:

- reading upstream code with Codex
- writing EvoHarness code
- inspecting experiment logic
- lightweight debugging when convenient

The Linux GPU server is mainly used for:

- running AppWorld experiments
- running local model inference
- large-scale evaluation

---

## 3. Main Research Route

The project is organized into three levels.

### Level 1 — Within-task Context Optimization

Goal:

Reduce unnecessary active context while preserving task-critical state.

Primary reference:

- ACON

Reference source:

- `G:\harness\third_party\acon`

Questions to study:

- Which observations should remain verbatim?
- Which observations can be compressed?
- When should compression happen?
- How should compressed state be represented?
- What information is commonly lost during compression?
- Can context compression reduce token usage without harming success rate?

Initial comparison:

- full-history baseline
- naive truncation
- simple summarization
- ACON-style context optimization
- EvoHarness context policy

---

### Level 2 — Cross-task Experience

This stage starts only after Level 1 works.

Goal:

Extract reusable experience from successful and failed trajectories and inject relevant experience into future tasks.

Potential references:

- ACE
- ReasoningBank

Possible experience types:

- reusable strategies
- common failure patterns
- tool-use pitfalls
- domain-specific procedural knowledge
- error-recovery rules

The memory should not simply store raw trajectories.

The intended abstraction is a structured Experience Playbook.

---

### Level 3 — Harness Evolution

This stage starts only after Levels 1 and 2 work.

Goal:

Use accumulated trajectories and failure analysis to improve harness-level instructions and policies.

Primary reference:

- GEPA-style reflective optimization

Potential optimization targets:

- system instructions
- tool-use instructions
- context-compression guidelines
- memory-retrieval instructions
- error-recovery rules
- stopping rules

The optimizer should not modify model weights.

---

## 4. Proposed EvoHarness Contribution

The planned original contribution is:

### Failure-Routed Harness Adaptation

Instead of updating every component after a failed task, first attribute the failure to a likely harness component.

Example failure sources:

- context information loss
- missing reusable experience
- incorrect tool-use policy
- repeated ineffective actions
- premature stopping
- bad recovery after API/tool errors

Then route the failure to the appropriate optimization target.

Conceptually:

```text
trajectory failure
       |
       v
failure attribution
       |
       +--> context issue ----> update context policy
       |
       +--> experience issue --> update playbook
       |
       +--> harness issue -----> update harness instruction
```

This is the main integration point between context optimization, experience learning, and reflective harness evolution.

---

## 5. Experimental Variants

The initial experiment matrix should remain simple.

### V0 — Baseline

- AppWorld simplified function-calling agent
- full message history
- no experience memory
- static harness

### V1 — Context Harness

- context optimization enabled
- no experience memory
- static harness

### V2 — Context + Experience

- context optimization enabled
- Experience Playbook enabled
- static harness

### V3 — Full EvoHarness

- context optimization enabled
- Experience Playbook enabled
- reflective harness evolution enabled

Do not add extra modules unless they support a clearly defined ablation.

---

## 6. Core Metrics

At minimum record:

- task success
- number of agent turns
- number of tool calls
- invalid tool calls
- repeated tool calls
- input tokens
- output tokens
- total tokens
- peak active-context tokens
- compression ratio
- wall-clock latency

Later metrics may include:

- recovery after tool failure
- constraint violation count
- memory retrieval precision
- memory usefulness
- failure-attribution accuracy

---

## 7. Immediate Milestone

The first milestone is intentionally narrow.

Do only the following:

1. Read AppWorld simplified function-calling agent implementation.
2. Identify the exact agent loop.
3. Identify where messages are appended.
4. Identify how tool calls and tool outputs are represented.
5. Identify where the model request is constructed.
6. Identify how task success is evaluated.
7. Read ACON's AppWorld integration.
8. Identify exactly where ACON intercepts/compresses context.
9. Build EvoHarness V0 around AppWorld without changing benchmark semantics.
10. Establish trajectory logging and baseline metrics.

Only after V0 is reproducible should V1 context optimization be implemented.

---

## 8. Non-goals

Do not spend time on:

- frontend/UI
- MCP integration
- multi-agent orchestration
- browser automation
- SWE-Bench
- Docker infrastructure
- model training
- RL
- large-scale deployment
- production serving
- unrelated framework abstractions

These may be added later only if the project direction changes explicitly.

---

## 9. Local and Server Separation

Local Windows workspace:

`G:\harness`

Expected structure:

```text
G:\harness
├── AGENTS.md
├── EvoHarness
└── third_party
    ├── appworld
    └── acon
```

Server layout should be conceptually similar, but paths may differ.

EvoHarness code must not depend on Windows-specific absolute paths.

Use configuration for:

- AppWorld root
- results directory
- model endpoint
- model name
- API key
- experiment config

---

## 10. Decision Rule

Whenever a design decision appears complicated, prefer the option that makes the experimental causal story clearer.

The main question is not:

> Can we build a complicated agent?

The main question is:

> Which harness changes make a frozen LLM agent measurably better, and why?

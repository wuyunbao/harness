# EvoHarness Development Constraints

- Only modify this EvoHarness repository. Treat `../third_party/appworld` and
  `../third_party/acon` as read-only upstream source references.
- Preserve the official AppWorld benchmark, environment, agent-loop, and
  evaluation semantics.
- Keep the base LLM frozen. Do not add GRPO, PPO, SFT, RL training, or other
  model-weight updates.
- V0 is the identity-context baseline: active messages equal the complete
  canonical message history.
- Reuse AppWorld's official `LanguageModel`, `APIPredictor`, `UsageTracker`,
  environment, and evaluator. Do not copy or reimplement them.
- Keep changes small and testable; avoid unrelated abstractions and features.
- Local Windows is for development and lightweight checks. Formal experiments
  run on a Linux server, so project code must remain portable.
- Never hard-code `G:\harness` or another machine-specific absolute path in
  source code. Use configuration, arguments, environment variables, or
  relative paths.

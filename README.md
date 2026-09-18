# EvoHarness

EvoHarness is a research harness for studying how context management can
improve long-horizon AppWorld agents while keeping the base language model
frozen.

The project is currently at V0: an identity-context baseline built as a thin
adapter around AppWorld's official simplified function-calling agent.

## Installation

AppWorld and its agent package must already be available in the target
environment. Install EvoHarness itself in editable mode:

```bash
pip install -e .
```

## Single-task V0 smoke run

Use an existing AppWorld simplified function-calling experiment config and
override only its registered agent type:

```bash
python -m evoharness.runner --source-experiment <official-appworld-experiment-name> --experiment-name evoharness_v0_smoke --task-id <appworld-task-id>
```

The command delegates task loading and execution to AppWorld's official
simplified runner. It does not run evaluation automatically.

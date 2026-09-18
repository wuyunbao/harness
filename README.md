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

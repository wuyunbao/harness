"""EvoHarness wrapper for AppWorld's simplified function-calling agent."""

from typing import Any

from appworld_agents.code.simplified.agent import Agent
from appworld_agents.code.simplified.function_calling_agent import (
    SimplifiedFunctionCallingAgent,
)

from evoharness.agent.language_model import LanguageModelRequestAdapter
from evoharness.context import ContextManager, IdentityContextManager


AGENT_TYPE = "evoharness_function_calling"


@Agent.register(AGENT_TYPE)
class EvoHarnessFunctionCallingAgent(SimplifiedFunctionCallingAgent):  # type: ignore[misc]
    """Official AppWorld agent with an active-context request boundary."""

    def __init__(
        self,
        *args: Any,
        context_manager: ContextManager | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.context_manager = (
            context_manager if context_manager is not None else IdentityContextManager()
        )
        self.language_model = LanguageModelRequestAdapter(
            delegate=self.language_model,
            context_manager=self.context_manager,
        )

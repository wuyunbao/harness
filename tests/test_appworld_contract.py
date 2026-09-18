import inspect
import unittest


try:
    from appworld_agents.code.simplified.agent import Agent
    from appworld_agents.code.simplified.function_calling_agent import (
        SimplifiedFunctionCallingAgent,
    )
    from appworld_agents.code.simplified.language_model import LanguageModel
except ImportError as exception:
    APPWORLD_IMPORT_ERROR: ImportError | None = exception
else:
    APPWORLD_IMPORT_ERROR = None


@unittest.skipIf(
    APPWORLD_IMPORT_ERROR is not None,
    f"external AppWorld packages are unavailable: {APPWORLD_IMPORT_ERROR}",
)
class AppWorldContractTest(unittest.TestCase):
    def test_official_agent_and_language_model_contract(self) -> None:
        from evoharness.agent.function_calling import (
            AGENT_TYPE,
            EvoHarnessFunctionCallingAgent,
        )

        self.assertTrue(
            issubclass(EvoHarnessFunctionCallingAgent, SimplifiedFunctionCallingAgent)
        )
        self.assertIs(Agent.by_name(AGENT_TYPE), EvoHarnessFunctionCallingAgent)
        self.assertTrue(callable(getattr(LanguageModel, "generate", None)))
        self.assertTrue(callable(getattr(LanguageModel, "log_calls_to", None)))
        self.assertIn("self.tool_parser", inspect.getsource(LanguageModel.__init__))


if __name__ == "__main__":
    unittest.main()

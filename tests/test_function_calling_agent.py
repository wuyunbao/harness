import importlib
import sys
import types
import unittest
from unittest.mock import patch

from evoharness.agent.language_model import LanguageModelRequestAdapter
from evoharness.context import IdentityContextManager


class FakeAgent:
    registered: dict[str, type] = {}

    @classmethod
    def register(cls, name: str):
        def register_subclass(subclass: type) -> type:
            cls.registered[name] = subclass
            return subclass

        return register_subclass


class FakeSimplifiedFunctionCallingAgent(FakeAgent):
    def __init__(self, *args: object, **kwargs: object) -> None:
        self.super_args = args
        self.super_kwargs = kwargs
        self.language_model = object()
        self.api_predictor = object()


class EvoHarnessFunctionCallingAgentTest(unittest.TestCase):
    def test_subclasses_registers_and_only_wraps_main_language_model(self) -> None:
        agent_module = types.ModuleType("appworld_agents.code.simplified.agent")
        agent_module.Agent = FakeAgent
        function_calling_module = types.ModuleType(
            "appworld_agents.code.simplified.function_calling_agent"
        )
        function_calling_module.SimplifiedFunctionCallingAgent = (
            FakeSimplifiedFunctionCallingAgent
        )
        fake_modules = {
            "appworld_agents": types.ModuleType("appworld_agents"),
            "appworld_agents.code": types.ModuleType("appworld_agents.code"),
            "appworld_agents.code.simplified": types.ModuleType(
                "appworld_agents.code.simplified"
            ),
            "appworld_agents.code.simplified.agent": agent_module,
            "appworld_agents.code.simplified.function_calling_agent": (
                function_calling_module
            ),
        }

        sys.modules.pop("evoharness.agent.function_calling", None)
        FakeAgent.registered.clear()
        with patch.dict(sys.modules, fake_modules):
            module = importlib.import_module("evoharness.agent.function_calling")
            agent_class = module.EvoHarnessFunctionCallingAgent
            agent = agent_class(example="value")

        self.assertTrue(issubclass(agent_class, FakeSimplifiedFunctionCallingAgent))
        self.assertIs(FakeAgent.registered[module.AGENT_TYPE], agent_class)
        self.assertEqual(module.AGENT_TYPE, "evoharness_function_calling")
        self.assertEqual(agent.super_kwargs, {"example": "value"})
        self.assertIsInstance(agent.context_manager, IdentityContextManager)
        self.assertIsInstance(agent.language_model, LanguageModelRequestAdapter)
        self.assertIsNot(agent.language_model, agent.api_predictor)
        self.assertEqual(
            set(agent_class.__dict__) & {
                "initialize",
                "next_execution_inputs_usage_and_status",
                "first_execution_inputs_usage_and_status",
                "second_onwards_execution_inputs_usage_and_status",
            },
            set(),
        )


if __name__ == "__main__":
    unittest.main()

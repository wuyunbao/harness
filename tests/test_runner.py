from copy import deepcopy
import importlib
import inspect
import sys
import types
import unittest
from unittest.mock import patch

from evoharness import runner


class FakeAgent:
    registered: dict[str, type] = {}

    @classmethod
    def register(cls, name: str):
        def register_subclass(subclass: type) -> type:
            cls.registered[name] = subclass
            return subclass

        return register_subclass


class FakeSimplifiedFunctionCallingAgent(FakeAgent):
    pass


class RunnerTest(unittest.TestCase):
    def test_single_task_overlays_agent_type_and_delegates_to_official_runner(self) -> None:
        source_config = {
            "type": "simplified",
            "config": {
                "agent": {
                    "type": "simplified_function_calling",
                    "model_config": {"name": "fake-model"},
                },
                "dataset": "dev",
            },
            "metadata": {"source": "official"},
        }
        source_config_before = deepcopy(source_config)
        calls: list[dict[str, object]] = []
        loaded_experiments: list[str] = []

        def load_experiment_config(name: str) -> dict[str, object]:
            loaded_experiments.append(name)
            return source_config

        appworld_cli_module = types.ModuleType("appworld.cli")
        appworld_cli_module.load_experiment_config = load_experiment_config
        agent_module = types.ModuleType("appworld_agents.code.simplified.agent")
        agent_module.Agent = FakeAgent
        function_calling_module = types.ModuleType(
            "appworld_agents.code.simplified.function_calling_agent"
        )
        function_calling_module.SimplifiedFunctionCallingAgent = (
            FakeSimplifiedFunctionCallingAgent
        )
        run_module = types.ModuleType("appworld_agents.code.simplified.run")
        run_module.run_experiment = lambda **kwargs: calls.append(kwargs)
        fake_modules = {
            "appworld": types.ModuleType("appworld"),
            "appworld.cli": appworld_cli_module,
            "appworld_agents": types.ModuleType("appworld_agents"),
            "appworld_agents.code": types.ModuleType("appworld_agents.code"),
            "appworld_agents.code.simplified": types.ModuleType(
                "appworld_agents.code.simplified"
            ),
            "appworld_agents.code.simplified.agent": agent_module,
            "appworld_agents.code.simplified.function_calling_agent": (
                function_calling_module
            ),
            "appworld_agents.code.simplified.run": run_module,
        }

        sys.modules.pop("evoharness.agent.function_calling", None)
        FakeAgent.registered.clear()
        try:
            with patch.dict(sys.modules, fake_modules):
                runner.run_single_task(
                    source_experiment="official/config",
                    experiment_name="evoharness_v0_smoke",
                    task_id="task-1",
                )
                registered_module = importlib.import_module(
                    "evoharness.agent.function_calling"
                )
        finally:
            sys.modules.pop("evoharness.agent.function_calling", None)

        self.assertIn("evoharness_function_calling", FakeAgent.registered)
        self.assertIs(
            FakeAgent.registered["evoharness_function_calling"],
            registered_module.EvoHarnessFunctionCallingAgent,
        )
        self.assertEqual(source_config, source_config_before)
        self.assertEqual(loaded_experiments, ["official/config"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(
            calls[0],
            {
                "experiment_name": "evoharness_v0_smoke",
                "runner_config": {
                    "agent": {
                        "type": "evoharness_function_calling",
                        "model_config": {"name": "fake-model"},
                    },
                    "dataset": "dev",
                },
                "task_id": "task-1",
                "num_processes": 1,
                "process_index": 0,
            },
        )

    def test_runner_contains_no_appworld_task_loop(self) -> None:
        source = inspect.getsource(runner)

        self.assertNotIn(".solve_task(", source)
        self.assertNotIn(".solve_tasks(", source)
        self.assertNotIn("AppWorld(", source)


if __name__ == "__main__":
    unittest.main()

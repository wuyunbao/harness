"""Single-task V0 smoke runner backed by AppWorld's official simplified runner."""

import argparse
from copy import deepcopy
from typing import Any


def _apply_v0_overlay(
    experiment_config: dict[str, Any], agent_type: str
) -> dict[str, Any]:
    """Copy an official simplified config and replace only its agent type."""
    if experiment_config.get("type") != "simplified":
        raise ValueError("The source experiment must use AppWorld's simplified runner.")

    runner_config = deepcopy(experiment_config.get("config"))
    if not isinstance(runner_config, dict):
        raise ValueError("The source experiment is missing a runner config.")
    if not isinstance(runner_config.get("agent"), dict):
        raise ValueError("The source runner config is missing an agent config.")
    if "dataset" not in runner_config:
        raise ValueError("The source runner config is missing a dataset.")

    model_server_config = runner_config.pop("model_server", None)
    if model_server_config and model_server_config.get("enabled", False):
        raise ValueError(
            "The smoke runner does not manage AppWorld model servers; "
            "use a config whose model endpoint is already available."
        )

    runner_config["agent"]["type"] = agent_type
    return runner_config


def run_single_task(
    *, source_experiment: str, experiment_name: str, task_id: str
) -> None:
    """Run one task through AppWorld's official simplified experiment runner."""
    if not task_id.strip():
        raise ValueError("task_id must be non-empty.")

    from appworld.cli import load_experiment_config
    from appworld_agents.code.simplified.run import run_experiment

    from evoharness.agent.function_calling import AGENT_TYPE

    experiment_config = load_experiment_config(source_experiment)
    runner_config = _apply_v0_overlay(experiment_config, AGENT_TYPE)
    run_experiment(
        experiment_name=experiment_name,
        runner_config=runner_config,
        task_id=task_id,
        num_processes=1,
        process_index=0,
    )


def main() -> None:
    """Parse the minimal smoke-run arguments and delegate to AppWorld."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-experiment",
        required=True,
        help="AppWorld experiment config name to use as the official baseline.",
    )
    parser.add_argument(
        "--experiment-name",
        required=True,
        help="Name for the EvoHarness smoke-run outputs.",
    )
    parser.add_argument("--task-id", required=True, help="One AppWorld task ID to run.")
    args = parser.parse_args()
    run_single_task(
        source_experiment=args.source_experiment,
        experiment_name=args.experiment_name,
        task_id=args.task_id,
    )


if __name__ == "__main__":
    main()

from copy import deepcopy
import unittest

from evoharness.agent.language_model import LanguageModelRequestAdapter
from evoharness.context import IdentityContextManager


class FakeLanguageModel:
    def __init__(self, result: object = None, error: Exception | None = None) -> None:
        self.result = result
        self.error = error
        self.calls: list[tuple[object, tuple[object, ...], dict[str, object]]] = []
        self.tool_parser = object()

    def generate(self, messages: object, *args: object, **kwargs: object) -> object:
        self.calls.append((messages, args, kwargs))
        if self.error is not None:
            raise self.error
        return self.result

    def log_calls_to(self, *, world: object) -> tuple[str, object]:
        return ("logged", world)


class LanguageModelRequestAdapterTest(unittest.TestCase):
    def test_forwards_request_exactly_and_returns_same_result(self) -> None:
        expected = {
            "role": "assistant",
            "content": "",
            "standardized_usage": object(),
        }
        messages = [{"role": "user", "content": "task"}]
        messages_before = deepcopy(messages)
        tools = [{"type": "function", "function": {"name": "app__api"}}]
        delegate = FakeLanguageModel(result=expected)
        adapter = LanguageModelRequestAdapter(delegate, IdentityContextManager())

        actual = adapter.generate(
            messages,
            tools=tools,
            cache_control_at=-1,
            temperature=0,
        )

        self.assertIs(actual, expected)
        self.assertEqual(len(delegate.calls), 1)
        forwarded_messages, forwarded_args, forwarded_kwargs = delegate.calls[0]
        self.assertIs(forwarded_messages, messages)
        self.assertEqual(forwarded_args, ())
        self.assertIs(forwarded_kwargs["tools"], tools)
        self.assertEqual(forwarded_kwargs["cache_control_at"], -1)
        self.assertEqual(forwarded_kwargs["temperature"], 0)
        self.assertEqual(messages, messages_before)

    def test_forwards_positional_arguments(self) -> None:
        messages = [{"role": "user", "content": "task"}]
        tools = [{"type": "function", "function": {"name": "app__api"}}]
        delegate = FakeLanguageModel(result={})
        adapter = LanguageModelRequestAdapter(delegate, IdentityContextManager())

        adapter.generate(messages, tools, -1)

        forwarded_messages, forwarded_args, forwarded_kwargs = delegate.calls[0]
        self.assertIs(forwarded_messages, messages)
        self.assertEqual(forwarded_args, (tools, -1))
        self.assertEqual(forwarded_kwargs, {})

    def test_delegates_other_attributes_and_methods(self) -> None:
        delegate = FakeLanguageModel(result={})
        adapter = LanguageModelRequestAdapter(delegate, IdentityContextManager())
        world = object()

        self.assertIs(adapter.tool_parser, delegate.tool_parser)
        self.assertEqual(adapter.log_calls_to(world=world), ("logged", world))

    def test_propagates_delegate_exception_unchanged(self) -> None:
        error = RuntimeError("delegate failure")
        delegate = FakeLanguageModel(error=error)
        adapter = LanguageModelRequestAdapter(delegate, IdentityContextManager())

        with self.assertRaises(RuntimeError) as raised:
            adapter.generate([{"role": "user", "content": "task"}])

        self.assertIs(raised.exception, error)


if __name__ == "__main__":
    unittest.main()

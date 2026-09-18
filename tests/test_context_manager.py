from copy import deepcopy
import unittest

from evoharness.context import IdentityContextManager


class IdentityContextManagerTest(unittest.TestCase):
    def test_returns_canonical_messages_unchanged(self) -> None:
        messages = [
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": "task"},
        ]
        before = deepcopy(messages)

        active_messages = IdentityContextManager().prepare(messages)

        self.assertIs(active_messages, messages)
        self.assertEqual(active_messages, before)
        self.assertEqual(messages, before)

    def test_preserves_parallel_tool_call_group_and_ids(self) -> None:
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "tool-call-1",
                        "type": "function",
                        "function": {"name": "calendar__find", "arguments": "{}"},
                    },
                    {
                        "id": "response-item-2",
                        "call_id": "call-2",
                        "type": "function",
                        "function": {"name": "email__find", "arguments": "{}"},
                    },
                ],
            },
            {
                "role": "tool",
                "tool_call_id": "tool-call-1",
                "name": "calendar__find",
                "content": "calendar result",
            },
            {
                "role": "tool",
                "tool_call_id": "call-2",
                "name": "email__find",
                "content": "email result",
            },
        ]
        before = deepcopy(messages)

        active_messages = IdentityContextManager().prepare(messages)

        self.assertIs(active_messages, messages)
        self.assertEqual(active_messages, before)
        self.assertEqual(messages, before)
        self.assertEqual(active_messages[0]["tool_calls"][0]["id"], "tool-call-1")
        self.assertEqual(active_messages[0]["tool_calls"][1]["id"], "response-item-2")
        self.assertEqual(active_messages[0]["tool_calls"][1]["call_id"], "call-2")
        self.assertEqual(active_messages[1]["tool_call_id"], "tool-call-1")
        self.assertEqual(active_messages[2]["tool_call_id"], "call-2")


if __name__ == "__main__":
    unittest.main()

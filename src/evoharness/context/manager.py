"""Minimal context-manager contract used by the EvoHarness agent adapter."""

from typing import Any, Protocol


Message = dict[str, Any]


class ContextManager(Protocol):
    """Build the message view sent to the main language model."""

    def prepare(self, canonical_messages: list[Message]) -> list[Message]:
        """Return an active view without mutating ``canonical_messages``."""
        ...


class IdentityContextManager:
    """V0 context manager that preserves the complete canonical history."""

    def prepare(self, canonical_messages: list[Message]) -> list[Message]:
        """Return the canonical history unchanged.

        The returned list is the same object by design. Callers must treat it as
        read-only so V0 sends exactly the history maintained by AppWorld.
        """
        return canonical_messages

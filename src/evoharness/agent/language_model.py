"""Request-boundary adapter for AppWorld's official language model."""

from typing import Any

from evoharness.context import ContextManager, Message


class LanguageModelRequestAdapter:
    """Apply a context manager before delegating to an official language model."""

    def __init__(self, delegate: Any, context_manager: ContextManager) -> None:
        self._delegate = delegate
        self._context_manager = context_manager

    @property
    def delegate(self) -> Any:
        """The unchanged official language-model instance."""
        return self._delegate

    def generate(
        self, messages: list[Message], *args: Any, **kwargs: Any
    ) -> dict[str, Any]:
        """Prepare the active messages and return the delegate result unchanged."""
        active_messages = self._context_manager.prepare(messages)
        return self._delegate.generate(active_messages, *args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Transparently expose all other official language-model behavior."""
        return getattr(self._delegate, name)

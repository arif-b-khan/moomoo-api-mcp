from typing import Any


class Context:
    def __init__(self, request_context: Any = None, fastmcp: Any = None):
        self.request_context = request_context
        self.fastmcp = fastmcp

    async def info(self, message: str) -> None:
        # Forward info messages to the session's send_log_message if available
        session = getattr(self.request_context, "session", None)
        if session and hasattr(session, "send_log_message"):
            # session.send_log_message is expected to be async in tests
            await session.send_log_message(message)

    # Allow using Context[...] in type annotations without error
    @classmethod
    def __class_getitem__(cls, item):
        return cls


class FastMCP:
    """Minimal FastMCP stub used by tests and server lifecycle."""

    def __init__(self, name: str, lifespan: Any = None, dependencies: list[str] | None = None):
        self.name = name
        self.lifespan = lifespan
        self.dependencies = dependencies or []
        self._tools = []

    def run(self) -> None:
        # Minimal run method for manual invocation; no-op for tests
        return None

    def tool(self):
        """Return a decorator that registers a tool function.

        The decorator simply appends the function to an internal list and returns it.
        """

        def decorator(func):
            self._tools.append(func)
            return func

        return decorator


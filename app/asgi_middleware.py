import logging
from typing import Callable
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger("uvicorn.access")


class ASGILogBodyMiddleware:
    """ASGI middleware that reads the full request body, logs a safe/truncated
    representation, and then replays the original receive messages so downstream
    apps/handlers can read the body as if untouched.

    This avoids consuming the request stream permanently.
    """

    def __init__(self, app: ASGIApp, max_log_chars: int = 2000):
        self.app = app
        self.max_log_chars = max_log_chars

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # Only handle HTTP requests
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        # Collect the incoming request messages so we can both log and replay
        messages = []
        body = b""
        while True:
            message = await receive()
            messages.append(message)
            if message.get("type") != "http.request":
                break
            body += message.get("body", b"") or b""
            if not message.get("more_body", False):
                break

        # Safe logging: try to decode as utf-8 with replacement and truncate
        try:
            text = body.decode("utf-8", errors="replace")
        except Exception:
            text = "<binary>"

        truncated = (
            text[: self.max_log_chars] + ("... (truncated)" if len(text) > self.max_log_chars else "")
        )
        log_message = f"[request-body] {scope.get('method')} {scope.get('path')} body: {truncated}"
        logger.info(log_message)

        # Replay the original messages for downstream consumers
        msgs = list(messages)

        async def _receive_replay():
            if msgs:
                return msgs.pop(0)
            # No more messages: return empty final message
            return {"type": "http.request", "body": b"", "more_body": False}

        await self.app(scope, _receive_replay, send)

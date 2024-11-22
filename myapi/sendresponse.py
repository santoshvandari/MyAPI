import json
from typing import Any, Callable


async def return_response(send: Callable, status: int, body: Any):
    """
    Helper to send a response.
    """
    body = json.dumps(body).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body,
        }
    )
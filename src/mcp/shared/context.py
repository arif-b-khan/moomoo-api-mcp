from dataclasses import dataclass
from typing import Any


@dataclass
class RequestContext:
    request_id: str
    meta: Any
    session: Any
    lifespan_context: Any

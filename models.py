from dataclasses import dataclass
from typing import Any


@dataclass
class ObserverInput:
    """Input wrapper for payload_observer workflow."""
    payload: Any


@dataclass
class ObserverOutput:
    """Output from payload_observer workflow."""
    payload: Any
    description: str

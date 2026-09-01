"""rpgpoc — minimal, testable core of the RPG-Engine.

Three pillars (per 07 §10): calc (how values are derived),
probes (how dice are rolled), rules (when a state switches behaviour).

This package deliberately keeps the architecture core small and pure so the
90% risk (event-log + reducer + calc + rules + multi-client store) can be
validated with unit tests before the GUI/print layers are built.
"""

__version__ = "0.0.1"

from .events import Event  # noqa: F401
from .store import LocalJsonStore  # noqa: F401
from .reducer import empty_state, fold, apply_event  # noqa: F401
from .loader import TemplateLoadError, load_template  # noqa: F401
from .client import Client, ClientError, client_sheet  # noqa: F401
from .chargen import (  # noqa: F401
    ChargenError,
    ChargenStepError,
    CharGen,
    points_needed,
    stat_bonus,
)

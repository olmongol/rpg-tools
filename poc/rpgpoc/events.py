"""Event model.

The append-only event *log* is the single source of truth. State is a pure
*fold* over the log (see reducer.py). Events are immutable, JSON-friendly, and
carry a monotonically increasing ``seq`` as the total order — NOT a wall-clock
timestamp — so that replaying the log is deterministic (07 §10.3: no time, no
randomness in the core math; ordering comes from ``seq``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


# Event types used by the PoC (kept small on purpose).
CHARACTER_CREATED = "character_created"
ITEM_ADDED = "item_added"
STAT_PROPOSED = "stat_proposed"
STAT_APPROVED = "stat_approved"
STAT_REJECTED = "stat_rejected"
BGO_PURCHASED = "bgo_purchased"
RULE_APPLIED = "rule_applied"


ALL_EVENT_TYPES = {
    CHARACTER_CREATED,
    ITEM_ADDED,
    STAT_PROPOSED,
    STAT_APPROVED,
    STAT_REJECTED,
    BGO_PURCHASED,
    RULE_APPLIED,
}


@dataclass(frozen=True)
class Event:
    """One log entry.

    ``payload`` is deliberately a plain dict: each event type has its own shape
    and the reducer knows how to interpret it. Keeping it untyped here keeps the
    store/transport layer generic; the *reducer* enforces the meaning.
    """

    seq: int
    char: str
    type: str
    actor: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seq": self.seq,
            "char": self.char,
            "type": self.type,
            "actor": self.actor,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Event":
        return cls(
            seq=int(d["seq"]),
            char=str(d["char"]),
            type=str(d["type"]),
            actor=str(d.get("actor", "")),
            payload=dict(d.get("payload", {})),
        )


class UnknownEventType(ValueError):
    """Raised by the reducer (or a validator) for a type it must handle but does not know."""

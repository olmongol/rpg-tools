"""Event reducer: ``state = fold(empty_state, log)``.

Pure functions only — no I/O, no time, no randomness. The event log is the
single source of truth; the state is a *view* derived from it. This is the
architecture the design commits to (append-only log + reducer), and it is what
makes the "2nd client sees the change" acceptance criterion trivial to prove:
both clients fold the same log and therefore get the same state.

Shape of state (po-c):
    {
      "char": str,
      "pending_stats": {stat_id: {"value": int, "actor": str, "seq": int}},
      "inventory": [{"id", "name", "actor", "seq"}],
      "bgo": [dict],                 # bgo_purchased payloads, append-only
      "character_created": {…} | None,
      "rules_fired": [{…}]           # rule_applied events (audit trail)
    }
"""

from __future__ import annotations

from typing import Any, Dict, List

from .events import (
    BGO_PURCHASED,
    CHARACTER_CREATED,
    ITEM_ADDED,
    STAT_APPROVED,
    STAT_PROPOSED,
    STAT_REJECTED,
    UnknownEventType,
)


def empty_state(char: str) -> Dict[str, Any]:
    return {
        "char": char,
        "pending_stats": {},
        "inventory": [],
        "bgo": [],
        "character_created": None,
        "rules_fired": [],
    }


def fold(char: str, log: List) -> Dict[str, Any]:
    """Fold a full log into a state. Deterministic; safe to call on a copy."""
    state = empty_state(char)
    for ev in log:
        state = apply_event(state, ev)
    return state


def apply_event(state: Dict[str, Any], ev) -> Dict[str, Any]:
    """Apply one event to a state and return a NEW state.

    We always return a fresh dict so callers can keep the old one (useful for
    client-side optimistic UI that compares two states). Nested structures we
    touch are shallow-copied; we never mutate ``state`` in place.
    """
    t = ev.type
    if t == CHARACTER_CREATED:
        return {
            **state,
            "character_created": {
                "actor": ev.actor,
                "seq": ev.seq,
                "payload": dict(ev.payload),
            },
        }

    if t == ITEM_ADDED:
        inv = list(state["inventory"])
        inv.append(
            {
                "id": ev.payload.get("id"),
                "name": ev.payload.get("name"),
                "actor": ev.actor,
                "seq": ev.seq,
            }
        )
        return {**state, "inventory": inv}

    if t == STAT_PROPOSED:
        pending = dict(state["pending_stats"])
        sid = ev.payload.get("stat")
        if not sid:
            raise ValueError(f"{t} payload missing 'stat' (seq={ev.seq})")
        pending[sid] = {
            "value": int(ev.payload["value"]),
            "actor": ev.actor,
            "seq": ev.seq,
            "status": "pending",
        }
        return {**state, "pending_stats": pending}

    if t == STAT_APPROVED:
        pending = dict(state["pending_stats"])
        sid = ev.payload.get("stat")
        if not sid:
            raise ValueError(f"{t} payload missing 'stat' (seq={ev.seq})")
        prior = pending.get(sid, {})
        pending[sid] = {
            "value": int(ev.payload.get("value", prior.get("value", 0))),
            "actor": ev.actor,
            "seq": ev.seq,
            "status": "approved",
        }
        return {**state, "pending_stats": pending}

    if t == STAT_REJECTED:
        pending = dict(state["pending_stats"])
        sid = ev.payload.get("stat")
        if not sid:
            raise ValueError(f"{t} payload missing 'stat' (seq={ev.seq})")
        pending[sid] = {
            "value": int(pending.get(sid, {}).get("value", ev.payload.get("value", 0))),
            "actor": ev.actor,
            "seq": ev.seq,
            "status": "rejected",
        }
        return {**state, "pending_stats": pending}

    if t == BGO_PURCHASED:
        bgo = list(state["bgo"])
        bgo.append({"actor": ev.actor, "seq": ev.seq, "payload": dict(ev.payload)})
        return {**state, "bgo": bgo}

    if t == "rule_applied":
        fired = list(state["rules_fired"])
        fired.append({"actor": ev.actor, "seq": ev.seq, "payload": dict(ev.payload)})
        return {**state, "rules_fired": fired}

    raise UnknownEventType(t)

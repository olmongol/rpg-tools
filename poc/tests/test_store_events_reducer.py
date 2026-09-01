"""Tests for the event model, local store, and reducer (task 3).

These test the ACTUAL API on disk (events.py / store.py / reducer.py):
  * Event(seq, char, type, actor, payload)  — frozen dataclass, to_dict/from_dict
  * LocalJsonStore(root).append / read_log / last_seq   (one events.jsonl per char)
  * reducer.fold(char, log) over character_created / item_added / stat_* /
    bgo_purchased / rule_applied ; unknown types raise UnknownEventType

The rules pillar (bleed_pause_on_heal, disease/poison stages) is task 7 —
NOT tested here. Scope kept honest.
"""
from __future__ import annotations

import dataclasses

import pytest

from rpgpoc import events as ev
from rpgpoc import reducer
from rpgpoc.store import LocalJsonStore


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def _ev(seq: int = 0, **kw) -> ev.Event:
    base = dict(seq=seq, char="char:alice", type="character_created",
                actor="player", payload={})
    base.update(kw)
    return ev.Event(**base)


def test_event_round_trips_through_dict() -> None:
    e = ev.Event(seq=3, char="char:x", type="item_added", actor="gm",
                 payload={"id": 17, "name": "torch"})
    d = e.to_dict()
    e2 = ev.Event.from_dict(d)
    assert e2 == e
    assert e2.payload == {"id": 17, "name": "torch"}
    assert e2.actor == "gm"


def test_event_defaults() -> None:
    e = ev.Event.from_dict({"seq": 1, "char": "c", "type": "character_created"})
    assert e.actor == ""            # actor defaults to empty string
    assert e.payload == {}          # payload defaults to empty dict


def test_event_is_frozen() -> None:
    e = _ev()
    with pytest.raises(dataclasses.FrozenInstanceError):
        e.seq = 99  # type: ignore[misc]


def test_event_type_constants_covers_full_set() -> None:
    assert {
        ev.CHARACTER_CREATED,
        ev.ITEM_ADDED,
        ev.STAT_PROPOSED,
        ev.STAT_APPROVED,
        ev.STAT_REJECTED,
        ev.BGO_PURCHASED,
        ev.RULE_APPLIED,
    } == ev.ALL_EVENT_TYPES


def test_unknown_event_type_is_a_value_error() -> None:
    assert issubclass(ev.UnknownEventType, ValueError)


# ---------------------------------------------------------------------------
# store (LocalJsonStore)
# ---------------------------------------------------------------------------

def test_store_append_then_read_log(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    s.append("alice", ev.Event(0, "alice", "character_created", "player",
                               {"level": 1}))
    s.append("alice", ev.Event(1, "alice", "item_added", "gm",
                               {"id": 5, "name": "torch"}))

    log = s.read_log("alice")
    assert [e.seq for e in log] == [0, 1]
    assert log[0].type == "character_created"
    assert log[1].payload == {"id": 5, "name": "torch"}


def test_store_is_append_only(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    s.append("a", ev.Event(0, "a", "character_created", "p", {}))
    first = (tmp_path / "chats" / "a" / "events.jsonl").read_text(encoding="utf-8")
    s.append("a", ev.Event(1, "a", "item_added", "p", {"id": 1}))
    after = (tmp_path / "chats" / "a" / "events.jsonl").read_text(encoding="utf-8")
    # the original line must still be the FIRST line, byte-for-byte
    assert after.startswith(first.rstrip("\n") + "\n")
    assert len(after.splitlines()) == 2


def test_store_last_seq(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    assert s.last_seq("a") == 0, "empty log -> last_seq 0"
    s.append("a", ev.Event(1, "a", "character_created", "p", {}))
    assert s.last_seq("a") == 1
    s.append("a", ev.Event(4, "a", "item_added", "p", {}))
    assert s.last_seq("a") == 4, "last_seq is the max seq, not count"


def test_store_empty_for_unknown_char(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    assert s.read_log("never") == []


def test_store_isolates_per_char(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    s.append("a", ev.Event(0, "a", "character_created", "p", {}))
    s.append("b", ev.Event(0, "b", "item_added", "p", {"id": 1}))
    assert len(s.read_log("a")) == 1
    assert len(s.read_log("b")) == 1
    assert s.read_log("a")[0].type == "character_created"


def test_store_rejects_path_traversal_name(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    with pytest.raises(ValueError):
        s.append("..", ev.Event(0, "..", "character_created", "p", {}))


def test_store_raises_on_corrupt_log_line(tmp_path) -> None:
    s = LocalJsonStore(tmp_path)
    s.append("c", ev.Event(0, "c", "character_created", "p", {}))
    path = tmp_path / "chats" / "c" / "events.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write("this is not json\n")
    with pytest.raises(ValueError, match="corrupt log line"):
        s.read_log("c")


# ---------------------------------------------------------------------------
# reducer
# ---------------------------------------------------------------------------

def test_empty_state_shape() -> None:
    s = reducer.empty_state("alice")
    assert s["char"] == "alice"
    assert s["pending_stats"] == {}
    assert s["inventory"] == []
    assert s["bgo"] == []
    assert s["character_created"] is None
    assert s["rules_fired"] == []


def test_fold_character_created() -> None:
    log = [ev.Event(0, "a", "character_created", "gm", {"level": 3, "hp": 20})]
    s = reducer.fold("a", log)
    assert s["character_created"] == {
        "actor": "gm",
        "seq": 0,
        "payload": {"level": 3, "hp": 20},
    }


def test_fold_item_added_appends_inventory() -> None:
    log = [
        ev.Event(0, "a", "character_created", "gm", {}),
        ev.Event(1, "a", "item_added", "p", {"id": 1, "name": "sword"}),
        ev.Event(2, "a", "item_added", "gm", {"id": 2, "name": "shield"}),
    ]
    s = reducer.fold("a", log)
    assert [i["id"] for i in s["inventory"]] == [1, 2]
    assert s["inventory"][0]["name"] == "sword"
    assert s["inventory"][1]["actor"] == "gm"


def test_stat_lifecycle_propose_approve_reject() -> None:
    log = [
        ev.Event(0, "a", "character_created", "gm", {}),
        ev.Event(1, "a", "stat_proposed", "p", {"stat": "STR", "value": 8}),
        ev.Event(2, "a", "stat_approved", "gm", {"stat": "STR", "value": 9}),
        ev.Event(3, "a", "stat_proposed", "p", {"stat": "DEX", "value": 5}),
        ev.Event(4, "a", "stat_rejected", "gm", {"stat": "DEX"}),
    ]
    s = reducer.fold("a", log)
    assert s["pending_stats"]["STR"]["status"] == "approved"
    assert s["pending_stats"]["STR"]["value"] == 9
    assert s["pending_stats"]["DEX"]["status"] == "rejected"


def test_stat_event_requires_stat_field() -> None:
    log = [ev.Event(0, "a", "stat_proposed", "p", {"value": 8})]  # no 'stat'
    with pytest.raises(ValueError):
        reducer.fold("a", log)


def test_fold_bgo_purchased_records_append_only() -> None:
    log = [
        ev.Event(0, "a", "character_created", "gm", {}),
        ev.Event(1, "a", "bgo_purchased", "p", {"bgo": "Ambitious"}),
        ev.Event(2, "a", "bgo_purchased", "p", {"bgo": "Lucky"}),
    ]
    s = reducer.fold("a", log)
    assert [b["payload"]["bgo"] for b in s["bgo"]] == ["Ambitious", "Lucky"]


def test_fold_rule_applied_appends_audit_trail() -> None:
    log = [
        ev.Event(0, "a", "character_created", "gm", {}),
        ev.Event(1, "a", "rule_applied", "engine", {"rule": "bleed_pause_on_heal"}),
    ]
    s = reducer.fold("a", log)
    assert s["rules_fired"] == [
        {"actor": "engine", "seq": 1,
         "payload": {"rule": "bleed_pause_on_heal"}}
    ]


def test_reducer_does_not_mutate_its_state() -> None:
    before = reducer.empty_state("a")
    snapshot_inventory = list(before["inventory"])
    reducer.apply_event(before, ev.Event(1, "a", "item_added", "p",
                                          {"id": 1, "name": "torch"}))
    # apply_event returns a new dict and must NOT touch the original list
    assert before["inventory"] == snapshot_inventory == []


def test_reducer_rejects_unknown_events() -> None:
    log = [ev.Event(0, "a", "something_entirely_new", "p", {})]
    with pytest.raises(ev.UnknownEventType):
        reducer.fold("a", log)


def test_fold_is_pure_and_deterministic() -> None:
    log = [
        ev.Event(0, "a", "character_created", "gm", {}),
        ev.Event(1, "a", "item_added", "p", {"id": 1, "name": "sword"}),
    ]
    log_copy = list(log)
    s1 = reducer.fold("a", log)
    s2 = reducer.fold("a", log_copy)
    assert s1 == s2
    assert s1 is not s2  # distinct objects, equal by value

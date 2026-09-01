"""Reactive rules engine — the third pillar (07 pillar 3).

A *rule* fires when its ``when`` condition is true for the (event, state) pair
and then declares an ``action`` (e.g. emit ``rule_applied`` / set a condition).
The engine is pure and deterministic: no I/O, no time, no RNG.

Design constraints (07):
  * Conditions are a small whitelist (parsed via ``ast``), NOT Python.
  * A rule may reference ``event.type``, ``event.payload.<k>``, and
    ``state.<dot.path>``.
  * ``event_types:`` lists the event types a rule reacts to.

Example (RM bleed-pause-on-heal, PoC-flavoured):
    rules:
      pause_bleed_on_heal:
        on: [hp_recovered]   # legacy; new templates use ``event_types:``
        when: "state.condition.bleeding == 1 and event.payload.amount > 0"
        action: {type: rule_applied, name: pause_bleed_on_heal}
"""
from __future__ import annotations

import ast
import operator
from typing import Any, Dict, List, Optional
from .events import Event
from .calc import _resolve, CalcSyntaxError, CalcReferenceError


class RuleError(ValueError):
    pass


_OPS = {
    ast.Eq: operator.eq, ast.NotEq: operator.ne,
    ast.Lt: operator.lt, ast.LtE: operator.le,
    ast.Gt: operator.gt, ast.GtE: operator.ge,
    ast.Is: operator.is_, ast.IsNot: operator.is_not,
}


def _eval_operand(node: ast.AST, ctx: dict) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in ("None", "True", "False"):
        return {"None": None, "True": True, "False": False}[node.id]
    if isinstance(node, ast.Name):
        return _resolve(node.id, ctx, "zero")
    if isinstance(node, ast.Attribute):
        parts: List[str] = []
        def _walk(n: ast.AST) -> None:
            if isinstance(n, ast.Attribute):
                parts.append(n.attr); _walk(n.value)
            elif isinstance(n, ast.Name):
                parts.append(n.id)
            else:
                raise RuleError("attribute leaf not a name")
        _walk(node)
        return _resolve(".".join(reversed(parts)), ctx, "zero")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_operand(node.operand, ctx)
    if isinstance(node, ast.BinOp):
        left = _eval_operand(node.left, ctx)
        right = _eval_operand(node.right, ctx)
        opmap = {ast.Add: operator.add, ast.Sub: operator.sub,
                 ast.Mult: operator.mul, ast.Div: operator.truediv}
        if type(node.op) not in opmap:
            raise RuleError(f"operator not allowed: {type(node.op).__name__}")
        return opmap[type(node.op)](left, right)
    raise RuleError(f"operand not supported: {type(node).__name__}")


def eval_condition(src: str, ctx: dict) -> bool:
    """Evaluate a whitelisted boolean comparison against a context dict.

    ``context`` typically maps ``event`` (an Event) and ``state`` (a dict) so
    expressions like ``state.hp.cur > 0 and event.payload.amount > 0`` work.
    We only support a single (possibly multi-op) Compare at the top level —
    no ``and``/``or`` in the PoC, keeping the whitelist tiny.
    """
    try:
        tree = ast.parse(str(src), mode="eval")
    except SyntaxError as exc:
        raise RuleError(f"condition not parseable: {src!r}: {exc}") from exc
    body = tree.body
    # Allow a single Compare (possibly chained) at top level.
    if not isinstance(body, ast.Compare) or len(body.ops) != 1:
        raise RuleError(f"condition shape not supported: {src!r}")
    op = body.ops[0]
    if type(op) not in _OPS:
        raise RuleError(f"comparison op not supported: {type(op).__name__}")
    left = _eval_operand(body.left, ctx)
    right = _eval_operand(body.comparators[0], ctx)
    try:
        return bool(_OPS[type(op)](left, right))
    except TypeError as exc:
        raise RuleError(f"comparison failed on {left!r} {type(op).__name__} {right!r}: {exc}") from exc


def _event_ctx(event: Event) -> dict:
    """Expose an Event's fields for condition resolution via dot-paths."""
    return {
        "type": event.type,
        "actor": event.actor,
        "payload": dict(event.payload),
    }


def matches(rule: dict, event: Event, state: dict) -> bool:
    """True if the rule should fire for this (event, state)."""
    allowed = rule.get("event_types")
    if allowed is None:  # legacy key name
        allowed = rule.get("on")
    if isinstance(allowed, (list, tuple)):
        if event.type not in allowed:
            return False
    elif isinstance(allowed, str):
        if event.type != allowed:
            return False
    when = rule.get("when")
    if when is None:
        return True
    ctx: dict = {"event": _event_ctx(event), "state": state}
    return eval_condition(str(when), ctx)


def fire(rule: dict, event: Event, state: dict) -> List[Dict[str, Any]]:
    """Return the list of action dicts to apply (usually one rule_applied)."""
    action = rule.get("action")
    if action is None:
        return []
    if not isinstance(action, dict):
        raise RuleError(f"rule action must be a mapping, got {action!r}")
    payload = dict(action)
    # Default to rule_applied if unspecified.
    payload.setdefault("type", "rule_applied")
    payload.setdefault("name", payload.get("name"))
    # Preserve the triggering context for the audit trail.
    payload["triggered_by"] = {"event_type": event.type, "event_seq": event.seq,
                               "actor": event.actor}
    return [payload]


def evaluate_rules(rules: dict, events: List[Event], state: dict) -> List[Dict[str, Any]]:
    """Run every rule against every event (in order) and collect actions."""
    fired: List[Dict[str, Any]] = []
    if not isinstance(rules, dict):
        return fired
    for name, rule in rules.items():
        if not isinstance(rule, dict):
            continue
        for ev in events:
            if matches(rule, ev, state):
                for action in fire(rule, ev, state):
                    action = dict(action)
                    action.setdefault("rule", name)
                    fired.append(action)
    return fired

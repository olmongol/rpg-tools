"""Calc evaluator — pure, deterministic, integer-valued.

Design (07 §10.2–10.3):
  * Structured terms, not strings as the primary carrier: each term is a
    ``{term: dot.path}`` reference plus optional ``condition`` and optional
    ``expr`` (a mini-language, NOT free-form Python).
  * A small AST parser with a WHITELISTED node type list implements the
    ``expr`` language. We never call ``eval()`` / ``exec()``. Allowed:
    ``+`` ``-`` ``*`` ``/``, parens, integer/float literals, dotted name
    references, and the two-arg function ``clamp(lo, x, hi)``.
  * Null policy: an unknown reference evaluates to ``0`` (configurable per
    block via ``null_policy: zero`` — the default — or ``raise``).
  * Rounding: per block (default ``floor``); applied at the end of the block
    to the accumulated term sum, BEFORE ``clamp``. Intermediate values may be
    rational (e.g. ``/ 2``); every *emitted* ``state.*`` value is ``int``.
  * ``clamp(low, x, high)`` is the last pipeline stage; we implement it as a
    function call inside the term's ``expr`` (per 07 §10.1 example ``{term:
    "clamp(-10, 25)"}`` — I'll also support ``{clamp: [-10, 25]}`` syntax as
    a convenience for templates that want to keep the arithmetic in the term).

The evaluator takes a *state* dict (the reduced state), a ``calc_spec`` dict
(the YAML-declared block), and returns an int.
"""

from __future__ import annotations

import ast
import math
import operator
from typing import Any, Dict, List, Optional


class CalcError(ValueError):
    """Base error for calc-evaluation failures."""


class CalcReferenceError(CalcError):
    """A term referenced a state field that does not exist (with
    ``null_policy: raise``), or the term's path cannot be resolved at all."""


class CalcSyntaxError(CalcError):
    """The ``expr`` mini-language failed to parse (whitelist violation)."""


# ---------------------------------------------------------------------------
# Expr mini-language  (whitelist via ast)
# ---------------------------------------------------------------------------

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_ALLOWED_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def _resolve(ref: str, state: Dict[str, Any], null_policy: str) -> Any:
    """Resolve a dotted reference against the state.

    ``null_policy = zero``  →  missing path evaluates to 0
    ``null_policy = raise`` →  CalcReferenceError
    """
    cur: Any = state
    for part in ref.split("."):
        if part == "":
            continue
        if isinstance(cur, dict):
            if part not in cur:
                if null_policy == "zero":
                    return 0
                raise CalcReferenceError(f"missing state path: {ref!r} (at {part!r})")
            cur = cur[part]
        elif isinstance(cur, (list, tuple)):
            try:
                idx = int(part)
            except ValueError:
                if null_policy == "zero":
                    return 0
                raise CalcReferenceError(f"non-integer list index {part!r} in {ref!r}")
            cur = cur[idx] if 0 <= idx < len(cur) else _null_return(null_policy, ref)
        else:
            if null_policy == "zero":
                return 0
            raise CalcReferenceError(f"can't index into {type(cur).__name__} in {ref!r}")
    return cur


def _null_return(policy: str, ref: str) -> Any:
    if policy == "zero":
        return 0
    raise CalcReferenceError(f"missing state path: {ref!r}")


def _expr_node(node: ast.AST, state: Dict[str, Any], null_policy: str) -> Any:
    if isinstance(node, ast.Expression):
        return _expr_node(node.body, state, null_policy)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise CalcSyntaxError(f"operator not allowed: {op_type.__name__}")
        op = _ALLOWED_BINOPS[op_type]
        a = _expr_node(node.left, state, null_policy)
        b = _expr_node(node.right, state, null_policy)
        try:
            return op(a, b)
        except ZeroDivisionError as exc:
            raise CalcSyntaxError(f"division by zero in expr") from exc
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY:
            raise CalcSyntaxError(f"unary op not allowed: {op_type.__name__}")
        return _ALLOWED_UNARY[op_type](_expr_node(node.operand, state, null_policy))
    if isinstance(node, ast.Constant):
        v = node.value
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return v
        raise CalcSyntaxError(f"constant type not allowed: {type(v).__name__}")
    if isinstance(node, ast.Name):
        return float(_resolve(node.id, state, null_policy))
    if isinstance(node, ast.Attribute):
        # dotted reference (a.b.c) appears as Attribute(Name(Attribute(Name)))
        parts: List[str] = []

        def _walk(n: ast.AST) -> None:
            if isinstance(n, ast.Attribute):
                parts.append(n.attr)
                _walk(n.value)
            elif isinstance(n, ast.Name):
                parts.append(n.id)
            else:
                raise CalcSyntaxError("attribute path has a non-name leaf")

        _walk(node)
        return float(_resolve(".".join(reversed(parts)), state, null_policy))
    if isinstance(node, ast.Call):
        name = node.func
        if isinstance(name, ast.Name) and name.id == "clamp" and not node.keywords:
            if len(node.args) != 3:
                raise CalcSyntaxError("clamp() needs exactly 3 args")
            lo = _expr_node(node.args[0], state, null_policy)
            x = _expr_node(node.args[1], state, null_policy)
            hi = _expr_node(node.args[2], state, null_policy)
            return float(max(lo, min(hi, x)))
        raise CalcSyntaxError(f"function call not allowed: {name}")
    raise CalcSyntaxError(f"node not allowed in expr: {type(node).__name__}")


def eval_expr(src: str, state: Dict[str, Any], null_policy: str = "zero") -> float:
    """Parse + evaluate the mini-language expression against ``state``.

    Returns float (caller rounds to int at the block level); ``state`` is
    never mutated.
    """
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError as exc:
        raise CalcSyntaxError(f"expr is not valid: {src!r}: {exc}") from exc
    return float(_expr_node(tree, state, null_policy))


# ---------------------------------------------------------------------------
# Block evaluation
# ---------------------------------------------------------------------------

def _round_half_away_from_zero(x: float) -> int:
    # "round" in the everyday sense; Python's round() is banker's rounding,
    # which is surprising for character stats. We want 1.5 -> 2, -1.5 -> -2.
    return int(math.copysign(math.floor(abs(x) + 0.5), x))


def evaluate_block(state: Dict[str, Any], block: Dict[str, Any]) -> int:
    """Evaluate one calc block from the template.

    block shape (see 07 §10):
        inputs: [...]
        pipeline: [ {expr: "...", [condition: "..."]}, ... ]   # terms, any order
        rounding: floor | round | ceil        # default floor
        clamp: [lo, hi]                       # optional, last stage

    Returns the final INT value.
    """
    terms: List[Dict[str, Any]] = block.get("pipeline") or block.get("terms") or []
    if not terms:
        raise CalcError("calc block declares no pipeline/terms")
    null_policy = str(block.get("null_policy", "zero"))
    rounding = str(block.get("rounding", "floor"))

    # Sum the terms; a term may be an ``expr`` (string) or ``{term: ref}``,
    # in which case each named reference contributes its value.
    total: float = 0.0
    for t in terms:
        if not isinstance(t, dict):
            raise CalcError(f"term must be a mapping, got {type(t).__name__}")
        if "expr" in t:
            expr = str(t["expr"])
            cond = t.get("condition")
            if cond is not None and not _cond_true(cond, state, null_policy):
                continue
            total += eval_expr(expr, state, null_policy)
        elif "term" in t:
            ref = str(t["term"])
            cond = t.get("condition")
            if cond is not None and not _cond_true(cond, state, null_policy):
                continue
            total += float(_resolve(ref, state, null_policy))
        else:
            raise CalcError(f"term has no expr/term: {t!r}")

    # Round to int (block-level rule; intermediate values are rational OK).
    if rounding == "floor":
        value = int(math.floor(total))
    elif rounding == "round":
        value = _round_half_away_from_zero(total)
    elif rounding == "ceil":
        value = int(math.ceil(total))
    else:
        raise CalcError(f"unknown rounding: {rounding!r}")

    clamp = block.get("clamp")
    if clamp is not None:
        if not (isinstance(clamp, (list, tuple)) and len(clamp) == 2):
            raise CalcError(f"clamp must be [lo, hi], got {clamp!r}")
        lo, hi = float(clamp[0]), float(clamp[1])
        value = int(max(lo, min(hi, value)))
    return value


def _cond_true(cond: Any, state: Dict[str, Any], null_policy: str) -> bool:
    """Simple condition language: ``"a.b.c != 0"``, ``"a.b.c == None"``,
    ``"a.b.c > 5"`` etc. We parse to a single Compare node and check it.
    Only a handful of ops are allowed; anything else → CalcSyntaxError.
    """
    ops = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
    }
    try:
        tree = ast.parse(str(cond), mode="eval")
    except SyntaxError as exc:
        raise CalcSyntaxError(f"condition is not valid: {cond!r}: {exc}") from exc
    body = tree.body if isinstance(tree, ast.Expression) else tree
    if not isinstance(body, ast.Compare) or len(body.ops) != 1:
        raise CalcSyntaxError(f"condition shape not supported: {cond!r}")
    op = body.ops[0]
    if type(op) not in ops:
        raise CalcSyntaxError(f"condition op not supported: {type(op).__name__}")
    left = _expr_node(body.left, state, null_policy)
    right = _expr_node(body.comparators[0], state, null_policy)
    try:
        return bool(ops[type(op)](left, right))
    except TypeError as exc:
        raise CalcSyntaxError(f"condition compare failed: {exc}") from exc

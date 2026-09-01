"""Dice / probe model.

A *probe* resolves "roll the die and compare":
    1. pick a die (e.g. d6) and an injectable RNG (deterministic in tests);
    2. roll -> integer in [1, sides];
    3. add a modifier (may be negative);
    4. optionally clamp to [lo, hi].

Kept deliberately tiny and pure. The RM template can point a probe at a stat
(e.g. RR[power] based on stats.re) via the calc pillar; the probe itself is
just "dN + modifier".
"""
from __future__ import annotations

import random
from typing import Optional


class Die:
    """A fair N-sided die. ``rng`` is injectable for determinism."""

    def __init__(self, sides: int, rng: Optional[random.Random] = None) -> None:
        if sides < 1 or not isinstance(sides, int):
            raise ValueError(f"dice sides must be a positive int, got {sides!r}")
        self.sides = sides
        self._rng = rng or random.Random()

    def roll(self) -> int:
        return int(self._rng.randint(1, self.sides))


def probe(
    sides: int,
    modifier: int = 0,
    lo: Optional[int] = None,
    hi: Optional[int] = None,
    rng: Optional[random.Random] = None,
) -> int:
    """Roll ``d{sides}``, add ``modifier``, optionally clamp to [lo, hi]."""
    value = Die(sides, rng=rng).roll() + int(modifier)
    if lo is not None:
        value = max(int(lo), value)
    if hi is not None:
        value = min(int(hi), value)
    return value


def make_probes_block(block: dict, state: dict) -> dict:
    """Evaluate a probes block from the template. Expected shape:

        probes:
          rr_power:
            die: 6
            modifier: 0            # or a calc ref resolved by caller
            clamp: [-5, 25]        # optional

    Returns {name: {"die": int, "modifier": int, "clamp": [lo, hi] | None}}.
    The actual *rolling* happens at call time (task 7 rules / live play),
    not here — this only validates/shapes the declared probes.
    """
    out: dict = {}
    for name, spec in (block or {}).items():
        if not isinstance(spec, dict):
            continue
        die = int(spec.get("die", 6))
        mod = spec.get("modifier", 0)
        if not isinstance(mod, (int, float)):
            raise ValueError(f"probe {name!r} modifier must be numeric, got {mod!r}")
        cp = spec.get("clamp")
        clamp = None
        if isinstance(cp, (list, tuple)) and len(cp) == 2:
            clamp = [int(cp[0]), int(cp[1])]
        out[name] = {"die": die, "modifier": int(mod), "clamp": clamp}
    return out

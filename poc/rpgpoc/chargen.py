"""CharGen — Wizard-Kern für Charaktererschaffung (Task 9).

Acht Schritte (definition.char_generation.steps):
    race -> folk -> occupation -> stats -> categories -> equipment -> bgos -> finalize

Design (Dok 05/07, engine_contract aus definition.yaml):
  * Rein + deterministisch: alle Würfe laufen über eine von außen
    übergebene Zufallsfunktion ``rng`` (Standard: random.Random()); der
    Core selbst hat KEINEN unbefugten Zufallszugriff — wer reproduzierbare
    Tests will, übergibt ``random.Random(seed)``.
  * Der Wizard ist ein *Zustandsaufbau*, keine Event-Log-Maschine: er
    sammelt die Schritt-Ausgaben und emittiert bei finalize genau EINEN
    ``character_created``-Event (rpgpoc.events.CHARACTER_CREATED), den der
    Reducer (rpgpoc.reducer) in ``state['character_created']`` ablegt.
    GM-Freigaben über Stat-Änderungen laufen über die
    stat_proposed/approved/rejected-Events, nicht hier.
  * BGOs nach Kosten-Tabelle (definition.bgo.cost_tiers):
    Nachteil kostet 0, Vorteil kostet nach Stufe (0/1/3/5/10/15).
    Bei budget_from_race darf die Summe der BGO-Kosten das Budget der
    Rasse (char_def/races.yaml bgo) nicht überschreiten.
  * Alle ausgegebenen Zahlen sind int (engine_contract.integer_output).

Nicht im PoC-Bereich (bleiben in GUI/Systemdaten):
  * Volk/Profession-Optionen (freie Texte, hier nur als Schlüssel
    durchgereicht, nicht validiert).
  * Ausrüstungspreise (definition.equipment fehlt -> purse = 0).
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from .events import CHARACTER_CREATED, Event


# Schritt-Reihenfolge, identisch zu definition.char_generation.steps.
# Ein anderes Template darf die Schritte deklarieren — CharGen liest sie
# aus der Definition (see _STEPS below).
_STEPS = ("race", "folk", "occupation", "stats",
          "categories", "equipment", "bgos", "finalize")


class ChargenError(ValueError):
    """Grundfehler des CharGen-Wizards (Schritt-Reihenfolge, Kosten, …)."""


class ChargenStepError(ChargenError):
    """Schritt wurde in der falschen Reihenfolge oder doppelt aufgerufen."""



# ---------------------------------------------------------------------------
# Stat-Mathematik (Legacy: rpgtoolbox/rolemaster.py statbonus / pointsneeded)
# ---------------------------------------------------------------------------

def stat_bonus(temp: int) -> int:
    r"""Bonus aus dem temp-Wert (1d100-Modifikator).

    Exakt Legacy (rolemaster.statbonus): 100 -> 10, 92 -> 6, 89 -> 4.
    Alle Ergebnisse sind int.
    """
    t = float(temp)
    if 0 < t <= 10:
        return int(round((t - 21) / 2))
    if 10 < t < 31:
        return int(round((t - 33) / 5))
    if 30 < t < 70:
        return 0
    if 69 < t < 90:
        return int(round((t - 67) / 5))
    if 89 < t < 101:
        return int(round((t - 81) / 2))
    return int(round((t - 95) * 2))


def points_needed(value: int) -> int:
    r"""Kosten in DP für einen Zielwert (Legacy pointsneeded).

    20..90 kosten 1:1; darüber: 90 + (v-90)^2; unter 20 wird auf 20 geklemmt.
    """
    v = max(20, int(value))
    if v <= 90:
        return v
    return 90 + (v - 90) ** 2


# ---------------------------------------------------------------------------
# Wizard
# ---------------------------------------------------------------------------

class CharGen:
    """Achtstufiger Charaktererstellungs-Wizard (deterministisch).

    Nutzung:
        cg = CharGen(seed=42)
        ev = cg.run({"race": "High Elves", "folk": "Silvanii",
                     "occupation": "Magician", "pool": 600,
                     "categories": ["Spells - Own Realm Open Lists"],
                     "bgos": [{"kind": "nachteil", "name": "Bereits verflucht"},
                              {"kind": "vorteil", "name": "Nahsicht", "cost": 1}],
                     "name": "Finrion"})
        state = fold("Finrion", [ev])   # rpgpoc.reducer
    """

    def __init__(
        self,
        definition: Optional[Dict[str, Any]] = None,
        char_def: Optional[Dict[str, Any]] = None,
        rng: Optional[random.Random] = None,
        seed: Optional[int] = None,
    ) -> None:
        if definition is None:
            raise ChargenError("definition fehlt (definition.yaml-Payload)")
        self.definition = definition
        self.char_def = char_def or {}
        if rng is None:
            rng = random.Random(seed if seed is not None else 0)
        self.rng = rng
        self._cursor = 0            # nächster Schritt-Index
        self._payload: Dict[str, Any] = {}
        self._steps_done: List[str] = []

    # -- innere Hilfsfunktionen -------------------------------------------

    def _next_step(self) -> str:
        if self._cursor >= len(_STEPS):
            raise ChargenStepError("alle Schritte bereits abgeschlossen")
        return _STEPS[self._cursor]

    def _ensure_step(self, expected: str) -> None:
        actual = self._next_step()
        if actual != expected:
            raise ChargenStepError(
                f"erwarteter Schritt {expected!r}, Wizard steht bei {actual!r}")

    def _advance(self, step: str, data: Any) -> None:
        self._payload[step] = data
        self._steps_done.append(step)
        self._cursor += 1

    def race_options(self) -> List[str]:
        """Schritt 1 vorbereiten: Rassen-Namen aus char_def (Anzeigedaten)."""
        self._ensure_step("race")
        races = self.char_def.get("races") or []
        if isinstance(races, dict):
            races = list(races.values())
        return [str(r.get("name")) for r in races if isinstance(r, dict)]

    def step_race(self, name: str) -> None:
        self._ensure_step("race")
        if not isinstance(name, str) or not name.strip():
            raise ChargenError("Rasse muss ein nicht-leerer Name sein")
        name = name.strip()
        names = self.race_options()
        if names and name not in names:
            raise ChargenError(
                f"unbekannte Rasse {name!r} (char_def.races: {names})")
        self._advance("race", name)

    def step_folk(self, name: str) -> None:
        self._ensure_step("folk")
        if not isinstance(name, str) or not name.strip():
            raise ChargenError("Volk muss ein nicht-leerer Name sein")
        self._advance("folk", name.strip())

    def step_occupation(self, name: str) -> None:
        self._ensure_step("occupation")
        if not isinstance(name, str) or not name.strip():
            raise ChargenError("Beruf muss ein nicht-leerer Name sein")
        self._advance("occupation", name.strip())

    # -- Schritt 4: stats (10x 1d100 + Rassenpunkte + DP-Verteilung) ------

    def race_info(self) -> Optional[Dict[str, Any]]:
        """Rassen-Eintrag aus char_def (stats/rr/bgo/hobby_ranks) oder None."""
        name = self._payload.get("race")
        if not name:
            return None
        races = self.char_def.get("races") or []
        if isinstance(races, dict):
            races = list(races.values())
        for r in races:
            if isinstance(r, dict) and r.get("name") == name:
                return r
        return None

    def step_stats(self, pool: Optional[int] = 600,
                   base: Optional[Dict[int, int]] = None) -> Dict[str, Any]:
        """Attribute würfeln (10x 1d100), Rassenpunkte anlegen, DP verteilen.

        Reihenfolge (Legacy chargen): 10x 1d100 -> +Rassen-Stat-Boni
        (char_def/races.yaml ``stats``, exakt raceAbilities) -> DP-Pool
        (pool, Legacy-Standard 600) als +1-Temp-Schritte verteilen.
        ``base``: {0..9: Temp-Wert} erzwingt feste Startwürfe (Tests).
        Ergebnis: {abbr: {base, race, temp, bonus, cost}} + pool_remaining.
        """
        self._ensure_step("stats")
        abbrs = [s["abbr"] for s in (self.definition.get("stats") or [])]
        if len(abbrs) != 10:
            raise ChargenError(
                f"erwarte 10 Stats in definition, habe {len(abbrs)}")
        if base is not None:
            if set(base.keys()) != set(range(10)):
                raise ChargenError("base-Mapping braucht genau die Keys 0..9")
            temps = [int(base[i]) for i in range(10)]
        else:
            temps = [self.rng.randint(1, 100) for _ in range(10)]
        pool = int(pool)
        if pool < 0:
            raise ChargenError("DP-Pool darf nicht negativ sein")

        # Rassenpunkte (Legacy raceAbilities: St:2 = +2 Punkte auf St).
        race = self.race_info() or {}
        race_pts = dict(race.get("stats") or {})
        bases = list(temps)
        alloc = [max(1, min(100, int(t) + int(race_pts.get(a, 0))))
                 for a, t in zip(abbrs, temps)]

        remaining = pool
        # Gierig: DP in den Temp-Wert, der die beste Bonus-Marge bringt.
        while remaining > 0:
            best_i, best_b = None, None
            for i, t in enumerate(alloc):
                if t >= 100:
                    continue
                nt = t + 1
                d_bonus = stat_bonus(nt) - stat_bonus(t)
                d_cost = points_needed(nt) - points_needed(t)
                if d_cost > remaining:
                    continue
                if best_b is None or d_bonus > best_b:
                    best_i, best_b = i, d_bonus
            if best_i is None:
                break
            alloc[best_i] += 1
            remaining -= points_needed(alloc[best_i]) - \
                points_needed(alloc[best_i] - 1)

        out: Dict[str, Any] = {}
        for i, a in enumerate(abbrs):
            t = int(alloc[i])
            out[a] = {
                "base": int(bases[i]),
                "race": int(race_pts.get(a, 0)),
                "temp": t,
                "bonus": stat_bonus(t),
                "cost": points_needed(t),
            }
        out["pool_remaining"] = remaining
        self._advance("stats", out)
        return out

    # -- Schritt 5: categories --------------------------------------------

    def step_categories(self, names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Gewählte Kategorien validieren (exakte Namen aus definition).

        Ergebnis: {name: {stats: [...]}} — Ränge bleiben 0 (Start);
        Prof-Bonuses kommen bei level-up per rules/calc, nicht hier.
        """
        self._ensure_step("categories")
        allowed = {c["name"] for c in (self.definition.get("categories") or [])}
        chosen = list(names or [])
        if not chosen:
            raise ChargenError("mind. eine Kategorie auswählen")
        out: Dict[str, Any] = {}
        for n in chosen:
            if n not in allowed:
                raise ChargenError(
                    f"unbekannte Kategorie {n!r} (definiert: {sorted(allowed)})")
            if n in out:
                continue
            row = next(c for c in self.definition["categories"] if c["name"] == n)
            out[n] = {"stats": list(row.get("stats", []))}
        self._advance("categories", out)
        return out


    # -- Schritt 6: equipment ---------------------------------------------

    def step_equipment(self, items: Optional[List[Dict[str, Any]]] = None,
                       purse: int = 0) -> Dict[str, Any]:
        """Anfängliche Ausrüstung + Beutel.

        PoC: items sind freie Dicts (name/anzahl/preis optional);
        purse = int, Startguthaben. Preise werden NICHT automatisch
        verrechnet (Preistabelle = Systemdaten, siehe char_def).
        """
        self._ensure_step("equipment")
        items = list(items or [])
        for it in items:
            if not isinstance(it, dict) or "name" not in it:
                raise ChargenError(
                    f"Ausrüstungs-Eintrag braucht 'name': {it!r}")
        purse = int(purse)
        if purse < 0:
            raise ChargenError("purse darf nicht negativ sein")
        out = {"items": items, "purse": purse}
        self._advance("equipment", out)
        return out

    # -- Schritt 7: bgos (Kosten-Tabelle) ----------------------------------

    def step_bgos(self, entries: Optional[List[Dict[str, Any]]] = None,
                  candidates: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """BGOs per Kosten-Tabelle (definition.bgo) validieren und summieren.

        Eintrag-Format:
            {"kind": "vorteil"|"nachteil", "name": str, "cost": int|None}
        - cost=None: wird aus ``candidates`` (name -> cost) übernommen,
          sonst Kosten-Stage 0. Würfeln (selection: roll) ist GUI-Seite —
          hier landet immer der konkrete, gültige Eintrag.
        - nachteil: Kosten immer definition.bgo.disadvantage_cost (RM: 0).
        - Kosten müssen eine Stage aus cost_tiers sein — sonst ChargenError.

        Budget: budget_from_race=true -> Summe der Kosten <= Rassen-Budget
        aus char_def/races.yaml. Überschreitung -> ChargenError.
        """
        self._ensure_step("bgos")
        bgo_def = self.definition.get("bgo") or {}
        cost_tiers = [int(c) for c in (bgo_def.get("cost_tiers") or [0, 1, 3, 5, 10])]
        cand = list(candidates or [])
        cand_by_name = {c.get("name"): c for c in cand if c.get("name")}

        race_name = self._payload.get("race")
        budget = None
        if bgo_def.get("budget_from_race"):
            races = self.char_def.get("races") or []
            if isinstance(races, dict):
                candidates_list = list(races.values())
            else:
                candidates_list = list(races)
            for r in candidates_list:
                if isinstance(r, dict) and r.get("name") == race_name \
                        and r.get("bgo") is not None:
                    budget = int(r["bgo"])
                    break

        chosen: List[Dict[str, Any]] = []
        total = 0
        for raw in (entries or []):
            kind = str(raw.get("kind", "vorteil")).lower()
            name = str(raw.get("name", "")).strip()
            if not name:
                raise ChargenError(f"BGO-Namen fehlt: {raw!r}")
            if kind not in ("vorteil", "nachteil", "advantage", "disadvantage"):
                raise ChargenError(f"unbekanntes BGO-Kind: {kind!r}")
            is_neg = kind in ("nachteil", "disadvantage")
            cost = raw.get("cost")
            if cost is None:
                c = cand_by_name.get(name)
                if c is not None and c.get("cost") is not None:
                    cost = c["cost"]
                else:
                    cost = 0 if is_neg else cost_tiers[0]
            cost = int(cost)
            if is_neg:
                cost = int(bgo_def.get("disadvantage_cost", 0))
            if cost not in cost_tiers:
                raise ChargenError(
                    f"BGO-Kosten {cost} nicht in cost_tiers {cost_tiers}")
            if budget is not None:
                if total + cost > budget:
                    raise ChargenError(
                        f"BGO-Budget {budget} der Rasse {race_name!r} "
                        f"überschritten (bisher {total}, +{cost})")
            total += cost
            chosen.append({"kind": "nachteil" if is_neg else "vorteil",
                           "name": name, "cost": cost})

        out = {"entries": chosen, "spent": total,
               "budget": budget if budget is not None else 0}
        self._advance("bgos", out)
        return out


    # -- Schritt 8: finalize -> character_created -------------------------

    def finalize(self, name: Optional[str] = None, actor: str = "player") -> Event:
        """Alle sieben Schritte + Name -> EINEN character_created-Event.

        Rückgabe: rpgpoc.events.Event(type=CHARACTER_CREATED, payload=…).
        Der Reducer legt das Payload unter state['character_created'] ab
        (inkl. actor/seq) — der GUI/Store hängt es an die Character-Datei.
        """
        self._ensure_step("finalize")
        missing = [s for s in _STEPS[:-1] if s not in self._payload]
        if missing:
            raise ChargenStepError(
                f"fehlende Schritte vor finalize: {missing}")
        name = (name or self._payload.pop("name", None) or "Charakter").strip()
        if not name:
            raise ChargenError("Charakter-Name darf nicht leer sein")
        payload: Dict[str, Any] = {
            "name": name,
            "system": str(self.definition.get("system", "rolemaster")),
            "steps": list(self._steps_done),
            "race": self._payload["race"],
            "folk": self._payload["folk"],
            "occupation": self._payload["occupation"],
            "stats": dict(self._payload["stats"]),
            "categories": dict(self._payload["categories"]),
            "equipment": dict(self._payload["equipment"]),
            "bgos": dict(self._payload["bgos"]),
        }
        self._cursor = len(_STEPS)
        return Event(
            seq=1,
            char=name,
            type=CHARACTER_CREATED,
            actor=actor,
            payload=payload,
        )

    def run(self, spec: Dict[str, Any]) -> Event:
        """Gesamter Lauf in einem Zug aus einem Spec-Dictionary (Tests/GUI).

        spec-Keys: race, folk, occupation, pool, stats_base (optional,
        {0..9: int} für deterministische Tests), categories, items, purse,
        bgos ([{"kind", "name", "cost"?}], cost aus bgo_candidates),
        bgo_candidates, name.
        """
        self.step_race(str(spec.get("race", "")))
        self.step_folk(str(spec.get("folk", "")))
        self.step_occupation(str(spec.get("occupation", "")))
        self.step_stats(pool=int(spec.get("pool", 600)),
                        base=spec.get("stats_base"))
        self.step_categories(list(spec.get("categories") or []))
        self.step_equipment(items=list(spec.get("items") or []),
                            purse=int(spec.get("purse", 0)))
        self.step_bgos(entries=list(spec.get("bgos") or []),
                       candidates=list(spec.get("bgo_candidates") or []))
        return self.finalize(name=spec.get("name"))

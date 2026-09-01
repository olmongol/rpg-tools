# Fehlende Tabellenwerte — Armor-Penalties (AT 9 / 13 / 17)

Stand: 2026-08-29 · Branch `hermes_dev`
Quelldatei: `src/rpgtoolbox/rpgtools.py`, Methode `equipmentPenalities.calcArmorPen()`
(Zeilen 333–422). Die Tabelle ist ein einfacher `if/elif`-Block auf `self.AT`.

## Kurzfassung — was fehlt (verifiziert, Code-Logik)

Die vier Penalty-Felder werden am Anfang auf **0** initialisiert (Zeilen 339–348).
Jede `elif`-Stufe setzt nur einen **Untermenge** davon. Nicht gesetzte Felder landen bei 0.

| AT | `minmanmod` | `maxmanmod` | `misatpen` | `armqupen` |
|----|:-----------:|:-----------:|:----------:|:----------:|
| **9**  | -5   | -50 | **fehlt (0)** | **fehlt (0)** |
| **13** | -10  | -70 | **fehlt (0)** | -5 |
| **17** | -15  | -90 | **fehlt (0)** | -10 |

Konkret in den drei `elif`-Blöcken:

* **AT 9** (Zeile 363–365): setzt nur `minmanmod` + `maxmanmod`.
  **Fehlt:** `self.misatpen` (Fernkampfangriffs-Penalty) **und** `self.armqupen` (Quickness-Penalty).
* **AT 13** (Zeile 381–384): setzt `minmanmod` + `maxmanmod` + `armqupen = -5`.
  **Fehlt:** `self.misatpen`.
* **AT 17** (Zeile 400–403): setzt `minmanmod` + `maxmanmod` + `armqupen = -10`.
  **Fehlt:** `self.misatpen`.

Folge im Laufzeitverhalten: Bei diesen AT-Stufen wird `misatpen` (=0) und bei AT 9 zusätzlich
`armqupen` (=0) aus dem Charakter-Dict (`character["misslepen"]` / `["armquickpen"]`) zurückgegeben,
obwohl RoLe-Richtwerte dort typischerweise negativ sein müssten. → **stille Nullen, keine Ausnahme.**

## Vollständige Tabelle laut aktuellem Code (Verifikation)

| AT | Level/Typ          | `minmanmod` | `maxmanmod`* | `misatpen` | `armqupen` |
|----|--------------------|:-----------:|:------------:|:----------:|:----------:|
| 6  | Armor‑Light        | 0           | -20          | -5         | 0          |
| 7  | Armor‑Light        | -10         | -40          | -15        | -10        |
| 8  | Armor‑Light        | -15         | -50          | -15        | -15        |
| 9  | Armor‑Light        | -5          | -50          | **0** ⚠    | **0** ⚠    |
| 10 | Armor‑Light        | -10         | -70          | -10        | -5         |
| 11 | Armor‑Light        | -15         | -90          | -20        | -15        |
| 12 | Armor‑Light        | -15         | -110         | -30        | -15        |
| 13 | Armor‑Medium       | -10         | -70          | **0** ⚠    | -5         |
| 14 | Armor‑Medium       | -15         | -90          | -10        | -10        |
| 15 | Armor‑Medium       | -25         | -120         | -20        | -20        |
| 16 | Armor‑Medium       | -25         | -130         | -20        | -20        |
| 17 | Armor‑Heavy        | -15         | -90          | **0** ⚠    | -10        |
| 18 | Armor‑Heavy        | -20         | -110         | -10        | -20        |
| 19 | Armor‑Heavy        | -35         | -150         | -30        | -30        |
| 20 | Armor‑Heavy        | -45         | -165         | -40        | -40        |

`*` = `maxmanmod` wird um `Skill[<Type>]["total bonus"]` aufgeschlagen; die Tabelle hier zeigt
nur den Basisteil. `⚠` = nicht im `elif`-Block gesetzt, bleibt auf den Initialwert 0.

## Was eingetragen werden MUSS (Werte aus der RoLe-Spielleiterregeln)

Die genauen Richtwerte für F‑K‑A‑P (Fernkampfangriffs-Penalty) bzw. Q (Quickness-Penalty) für
die jeweiligen AT-Stufen stehen in der RoLe-Richtwertetafel. Diese Werte sind in der Codebasis
nicht hinterlegt und von mir (ohne Buchvorlage) **nicht** zu belegen — daher hier nur Platzhalter:

```python
elif self.AT == 9:
    self.minmanmod = -5
    self.maxmanmod = -50 + self.character["cat"]["Armor - Light"]["Skill"]["Rigid Leather"]["total bonus"]
    self.misatpen  = <ROLE_FKAP_AT9>    # fehlt — aus RoLe-Richtwertetafel
    self.armqupen  = <ROLE_Q_AT9>       # fehlt — aus RoLe-Richtwertetafel

elif self.AT == 13:
    self.minmanmod = -10
    self.maxmanmod = -70 + self.character["cat"]["Armor - Medium"]["Skill"]["Chain"]["total bonus"]
    self.misatpen  = <ROLE_FKAP_AT13>   # fehlt — aus RoLe-Richtwertetafel
    self.armqupen  = -5                 # vorhanden

elif self.AT == 17:
    self.minmanmod = -15
    self.maxmanmod = -90 + self.character["cat"]["Armor - Heavy"]["Skill"]["Plate"]["total bonus"]
    self.misatpen  = <ROLE_FKAP_AT17>   # fehlt — aus RoLe-Richtwertetafel
    self.armqupen  = -10                # vorhanden
```

## Nicht verifizierte Beobachtung (Hypothese, keine Fehlernachweis)

Im `AT == 6`-Block (Zeile 350–352) steht `self.misatpen = -5`. Da AT 6 die leichteste Stufe
ist und in der Tabelle direkt darunter (AT 7) schon `-15` steht, wirkt der Wert `-5` hier
anomalous. **Das ist jedoch eine Vermutung** — ohne die RoLe-Richtwertetafel vorliegen zu haben
kann ich nicht bestätigen, dass RoLe dort `0` oder einen anderen Wert erwartet. → Vor dem
Ändern gegen das RoLe-Buch verifizieren. (Dieser Punkt steht hier ausdrücklich nur als
Hinweis, **nicht** als belegter Fehler.)

## Zusammenhang mit dem zweiten, separaten Fehler (GUI-Wiring)

Unabhängig von den fehlenden Tabellenwerten: `gui/modules/inventory_gui.py` hat drei
`calcMMP(self)`-Wrapper (Zeile 469, 1617, 4370), die `calc_mmp(self.character)` aufspalten
in 5 Werte `(mmp, at, misslepen, armqupen, armmanmod)`. Aber `rpgtoolbox/shop_logic.calc_mmp`
liefert **1 Float** (Maximum Market Power) zurück — ein `TypeError` beim Aufspalten (Kauf /
Verkauf / Equip). Die korrekte 5-Wert-Quelle ist `equipmentPenalities(...).calcArmorPen()`;
keine dieser drei Stellen ruft sie. Das ist der Crash, der die echten Penalties in der GUI
überhaupt nicht ans Ziel bringt — ein separater Fix, der neben den Tabellenwerten steht.

# Armor-Penalty-Tabelle — fehlende Tabellenwerte

**Stand:** 2026-09-01 — **GEFIXT** (User-Entscheidung: „setze alle fehlenden Werte standardmäßig auf 0").
**Scope:** `src/rpgtoolbox/rpgtools.py`, `equipmentPenalities.calcArmorPen()` (Klasse Zeile 263, Funktion 333–428).
**Regressionstest:** `src/rpgtoolbox/test_armor_penalty_zero_fill.py` (4/4 GREEN).

---

## Befund

Die Penalty-Tabelle in `calcArmorPen()` behandelt 15 AT-Stufen (6–20). Jede Zeile setzt
(oder soll setzen) vier Felder:

| Feld | Bedeutung |
|------|-----------|
| `minmanmod` | minimum maneuver modification |
| `maxmanmod` | maximum maneuver modification |
| `misatpen`  | missile attack penalty |
| `armqupen`  | armor/quickness penalty |

Diese vier sind oben in der Funktion auf `0` initialisiert (Zeilen 339–348). Ein Feld, das ein
`if/elif self.AT == N:`-Block **nicht** überschreibt, bleibt *stille Default-0*.

**AST-generierte Lücken-Map** (welche der 4 Felder ein AT-Block NICHT setzt):

| AT  | Zeile | `minmanmod` | `maxmanmod` | `misatpen` | `armqupen` |
|-----|-------|:-----------:|:-----------:|:---------:|:----------:|
| 6   | 350   | ❌ **fehlte** | ✓ −20 | ✓ −5 | ❌ **fehlte** |
| 7   | 353   | ✓ −10 | ✓ −40 | ✓ −15 | ✓ −10 |
| 8   | 358   | ✓ −15 | ✓ −50 | ✓ −15 | ✓ −15 |
| 9   | 363   | ✓ −5 | ✓ −50 | ❌ **fehlte** | ❌ **fehlte** |
| 10  | 369   | ✓ −10 | ✓ −70 | ✓ −10 | ✓ −5 |
| 11  | 374   | ✓ −15 | ✓ −90 | ✓ −20 | ✓ −15 |
| 12  | 379   | ✓ −15 | ✓ −110 | ✓ −30 | ✓ −15 |
| 13  | 384   | ✓ −10 | ✓ −70 | ❌ **fehlte** | ✓ −5 |
| 14  | 390   | ✓ −15 | ✓ −90 | ✓ −10 | ✓ −10 |
| 15  | 395   | ✓ −25 | ✓ −120 | ✓ −20 | ✓ −20 |
| 16  | 400   | ✓ −25 | ✓ −130 | ✓ −20 | ✓ −20 |
| 17  | 405   | ✓ −15 | ✓ −90 | ❌ **fehlte** | ✓ −10 |
| 18  | 411   | ✓ −20 | ✓ −110 | ✓ −10 | ✓ −20 |
| 19  | 416   | ✓ −35 | ✓ −150 | ✓ −30 | ✓ −30 |
| 20  | 421   | ✓ −45 | ✓ −165 | ✓ −40 | ✓ −40 |

> Die 3 Zeilen, die der User explizit nannte: **AT 9 (misatpen + armqupen), AT 13 (misatpen),
> AT 17 (misatpen)**. Plus **AT 6** (minmanmod + armqupen) — gleicher Befund, also mitbehandelt.

### Was bei AT 9/13/17 konkret fehlte

- **AT 9:** `misatpen` und `armqupen` wurden nicht gesetzt → blieben bei stummer Default-0.
- **AT 13:** `misatpen` wurde nicht gesetzt → Default-0. (`armqupen = -5` war bereits vorhanden.)
- **AT 17:** `misatpen` wurde nicht gesetzt → Default-0. (`armqupen = -10` war bereits vorhanden.)

> **Hinweis zum Clamp** (Zeile 427–428): nach der Tabelle gilt
> `if self.maxmanmod > self.minmanmod: self.maxmanmod = self.minmanmod`.
> Da alle `maxmanmod`-Basissätze (−20 … −165) *kleiner/gleich* `minmanmod` sind, greift er nie —
> er hebt keinen fehlenden Wert auf.

---

## Fix (dieses Commit)

Jeder der betroffenen Blöcke setzt die fehlenden Felder jetzt **explizit** auf `0` mit
`@bug`-Kommentar:

- `AT 6`  (Zeile 350): `+ self.minmanmod = 0`, `+ self.armqupen = 0` → `self.misatpen = -5` (vorhanden)
- `AT 9`  (Zeile 363): `+ self.misatpen = 0`, `+ self.armqupen = 0`
- `AT 13` (Zeile 384): `+ self.misatpen = 0`
- `AT 17` (Zeile 405): `+ self.misatpen = 0`

Das Verhalten bleibt mathematisch identisch (Default war eh 0); die Änderung macht die
Tabelle vollständig und abgleichsfähig.

### Verifikation (aus dem grünen Regressionstest)

```
AT 9  : misatpen=0  armqupen=0   minmanmod=-5   maxmanmod=-50   PASS
AT 13 : misatpen=0  armqupen=-5  minmanmod=-10  maxmanmod=-70   PASS
AT 17 : misatpen=0  armqupen=-10 minmanmod=-15  maxmanmod=-90   PASS
AT 6  : misatpen=-5 armqupen=0   minmanmod=0    maxmanmod=-20   PASS
AT 16 : misatpen=-20 armqupen=-20 minmanmod=-25 maxmanmod=-130  PASS  (Bestand, unverändert)
```

---

## Getrennter, NICHT behobener Befund

Die GUI crash-t bei Kauf/Verkauf/Equip, weil 3 Call-Sites in `src/gui/modules/inventory_gui.py`
(L469, L1617, L4370) `calcMMP(...)` entpacken als 5-Tupel, aber der zugeordnete
`shop_logic.calc_mmp` ist die **Marktmacht**-Preisleiste (liefert 1 Float) → `TypeError`.
Der eigentliche 5-Tupel-Provider `equipmentPenalities.calcArmorPen()` wird in der GUI nirgends
instanziiert (Klasse tot, außer `calcWeightPen`-Pfad). **Nicht** Bestandteil dieses
"Tabellenwerte auf 0" Fixes — eigener Follow-up (GUI-Wiring).

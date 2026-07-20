# Bugs — DP-Steigerungs-Logik

**Fundort:** `src/gui/epwins.py` — Klassenmethod `skillcatWin.__takeValsSkill` (Skill-Steigerung) und `skillcatWin.__takeValsCat` (Kategorie-Steigerung)
**Betroffen:** `rm_char_tools.py` als Launcher, DP-Logik liegt ausschließlich in `epwins.py`
**Datum:** 2026-07-20

---

## BUG-001: Skill-Kosten starten immer vom Index 0 statt vom lowval

**Priorität:** **Kritical**
**Datei/Zeilen:** `gui/epwins.py`, Zeilen 3014–3021

### Beschreibung
Bei der Skill-Steigerung wird `dpCosts` korrekt aus den Treeview-Daten geholt und `lowval` (Index, ab dem weitere Steigerungen beginnen sollen) wird bei teilweiser Vor-Leveling korrekt auf `self.__changed['cat'][cat]['Skill'][skill]['lvlups']` gesetzt. 

**ABER:** Die Kostenakquisation in den Zeilen 3014–3021 startet **immer vom Index 0** und ignoriert `lowval`:

```python
## Current (buggy):
if diff > 0:
    for i in range(0, diff):
        diffcost += int(dpCosts[i])
else:
    for i in range(diff, 0):
        diffcost -= int(dpCosts[i])
```

### Reproduktion
1. Skill "Kraftfertigkeit" in "Körperkraft" auf Rang 3 mit Standard-Progression `[16, 3, 24, 48, 80]`
2. Charakter hat `lvlups=2` (also bereits 2x gestiegen)
3. Benutzer erweitert den Rang von 3 auf 6: `diff = 6 - 3 = 3`
4. **Falsch:** Code累积iert von Index 0, also `16 + 3 + 24 = 43` DP
5. **Richtig:** Code sollte von Index 2 starten, also `24 + 48 + 80 = 152` DP

### Symptom
- **Undercharging bei teilweiser Vor-Leveling:** Charakter zahlt für die ersten DP-Tiere, nicht die aktuellen.
- Bei teureren Fortschreitungen (Early, Hard Knocks, etc.) ist der Fehler besonders gross und kann bis zu ×10x betragen.

### Fix
```python
if diff > 0:
    for i in range(lowval, lowval + diff):
        diffcost += int(dpCosts[i])
else:
    for i in range(lowval + diff, lowval):
        diffcost -= int(dpCosts[i])
```

**Hinweis:** Gleicher Bug bei Zeilen 3047–3055 und 3156–3166 (weitere Skill-Upgrade-Pfade).

---

## BUG-002: Kategorie-Kosten starten immer vom Index 0 statt vom lowval

**Priorität:** **Kritical**
**Datei/Zeilen:** `gui/epwins.py`, Zeilen 3264–3274

### Beschreibung
Gleiches Problem wie BUG-001, aber für Kategorie-Steigerungen in `__takeValsCat`. Der `lowval`-Wert wird korrekt aus `self.__changed['cat'][currcat]['lvlups']` ermittelt, aber die DP-Subtraktion ignoriert ihn und startet immer bei Index 0.

```python
## Current (buggy):
for i in range(0, diff):
    self.__usedDP += int(dpCosts[i])
for i in range(diff, 0):
    self.__usedDP -= int(dpCosts[i])
```

### Reproduktion
1. Kategorie "Körperkraft" auf Rang 5 mit Standard-Progression `[16, 3, 24, 48, 80]`
2. Charakter hat bereits `lvlups=3`
3. Benutzer erweitert auf Rang 8: `diff = 3`
4. **Falsch:** `16 + 3 + 24 = 43` DP
5. **Richtig:** `24 + 48 + 80 = 152` DP

### Fix
```python
lowval = self.__changed['cat'][currcat]['lvlups'] if "lvlups" in self.__changed['cat'][currcat] else 0

if diff > 0:
    for i in range(lowval, lowval + diff):
        self.__usedDP += int(dpCosts[i])
else:
    for i in range(lowval + diff, lowval):
        self.__usedDP -= int(dpCosts[i])
```

---

## BUG-003: Kategorie-Upgrade cap blockiert alle weiteren Steigerungen

**Priorität:** Medium
**Datei/Zeilen:** `gui/epwins.py`, Zeilen 3248–3253

### Beschreibung
```python
if self.__changed['cat'][currcat]['lvlups'] < len(dpCosts):
    diff = newval - self.__changed['cat'][currcat]['rank']
else:
    diff = 0
    newval = oldval
    newtotal = ...
```

Wenn `lowval >= len(dpCosts)` (also alle Fortschreitungsstufen verbraucht), wird `diff = 0` gesetzt und `newval` auf `oldval` (den Start-Rang) zurückgesetzt. Das bedeutet:

- **Keine weitere Levelung möglich**, wenn `lvlups >= len(dpCosts)`.
- Der Benutzer bekommt **keine Fehlermeldung**, die Änderung wird nur stillschweigend ignoriert.
- Treeview zeigt fälschlicherweise den neuen Rang, aber der interne Zustand bleibt auf dem alten Rang.

### Reproduktion
1. Kategorie mit 5-Tier-Progression (dpCosts enthält 5 Einträge)
2. Benutzer steigt von Rang 0 auf Rang 5: `diff = 5`, `lvlups = 5`
3. Nächster Versuch von Rang 5 auf Rang 6: `lvlups=5` ist **nicht** < `len(dpCosts)=5`
4. `diff = 0`, `newval = oldval = 5` — stiller Block

### Fix
```python
# Zeile 3251–3252 ersetzen:
else:
    # No more progression tiers available — show error to user
    ...
```
Alternativ: Fortschreitungslogik über mehrere Fortschrittstypen (Standard → Early → Hard Knocks → etc.) implementieren, damit `dpCosts` dynamisch erweitert wird.

---

## BUG-004: Category dpCosts-Type-Handling bei flachen Kosten

**Priorität:** Low
**Datei/Zeilen:** `gui/epwins.py`, Zeilen 3226–3230

### Beschreibung
```python
if type(dpCosts) == type(1):
    dpCosts = [dpCosts]
```

Wenn dpCosts ein einzelner integer ist (flat cost category), wird es in eine Liste konvertiert. Das funktioniert:
- **Korrekt für flat costs** (z.B. alle Stufen kosten gleiche DP)
- **Inkonsistent mit der Progressionslogik**, die variable Kosten erwartet

### Symptom
- Bei kategorien mit `dpCosts = 16` (flat) wird `[16]` erstellt.
- Die Schleife `range(lowval, lowval + diff)` akkumuliert `16` für jede Stufe. Das ist **korrekt** für flache Kosten, aber:
- Es funktioniert **nicht**, wenn die Kategorie variable Kosten erwartet, aber fälschlicherweise als `int` statt `list` serialisiert wurde.

### Prävention
Seriailisierung/deserialisierung der dpCosts konsistent als Liste halten, auch bei flachen Kosten.

---

## Zusammenfassung der Bugs

| Bug | Priorität | Bereich | Impact |
|-----|-----------|---------|--------|
| BUG-001 | Critical | Skill-Steigerung (alle Pfade) | **Undercharging bei teilweiser Vor-Leveling** — Charakter zahlt ~70x zu wenig DP |
| BUG-002 | Critical | Kategorie-Steigerung | **Undercharging bei teilweiser Vor-Leveling** — gleicher Effekt |
| BUG-003 | Medium | Kategorie-Upgrade | **Stille Blockierung** — keine weiteren Stufen möglich |
| BUG-004 | Low | dpCosts Typ-Konsistenz | Potentiell inkonsistente Serialisierung |

## Empfohlene Reihenfolge der Fixes
1. **BUG-001** (Skill-Steigerung) — Kritisch, betrifft direkt den Spielspaß
2. **BUG-002** (Kategorie-Steigerung) — Kritisch, aber seltener betroffen
3. **BUG-003** (Kategorie cap) — Medium, muss in jedem Fall gelöst werden
4. **BUG-004** (Typ-Handling) — Low, präventiv

---
Ende

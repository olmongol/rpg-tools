# BUGS - RPG Tools Bug-Register
> Scan Date: 2026-07-26 → 2026-08-13
> Target: src/ (46 Python files)

## [BUG-004] Debug-Stubs in attackcheck.py ✅ FIXED

- **Datei:** src/attackcheck.py, Zeile 1439+
- **Status:** Gefixt am 2026-08-12 — `print("DEBUG...` durch `logger.debug` ersetzt.
- **Beschreibung:** Uncommented `print(f"DEBUG: ...")` Statements. Console-Spam bei jedem Aufruf.

## [BUG-007] Unbenutzte .bak Files ✅ FIXED

- **Status:** Gefixt am 2026-08-12 — `epwins.py.bak3` gelöscht.
- **Beschreibung:** Backup-Dateien im Source-Tree verwirrten Code-Suche.

## [BUG-008] notdoneyet stubs

- **Status:** OFFEN (nicht crash-relevant)
- **Beschreibung:** ~97 `notdoneyet` Stub-Aufrufe in GUIs. Cleanup wäre Breaking Change, erstmal dokumentiert als Tracking-Eintrag.

## [BUG-012] PIL Image shadowing Bug ✅ FIXED

- **Status:** Gefixt am 2026-08-12 — Alle GUIs nutzen jetzt konsistent `from PIL import Image as _pilimg`. Keine wildcard-Import-Kollisionen mehr.
- **Beschreibung:** tkinter wildcard imports (`from tkinter import *`) überschrieben PIL.Image in den original Dateien.

## [BUG-013] monstercreator.py piclink crash ✅ FIXED

- **Status:** Gefixt am 2026-08-12 — Piclink jetzt mit `.get("piclink", "")` + None-Wach `if not picpath: raise ValueError(...)` + `ValueError` in except caught.
- **Beschreibung:** `Image.open(None/leer)` crashte beim Bildladen ohne Bild.

## [BUG-014] epcalcwin.py manlist IndexError ✅ FIXED

- **Status:** Gefixt am 2026-08-12 — `self.manlist[0]` ohne len-check gefixt mit leerem Guard und fallback default.
- **Beschreibung:** `maneuvers.keys()` konnte bei leeren dict_keys zu IndexError auf `[0]` führen.

## [BUG-015] DP-Abzug + GUI-Anzeige bei Cat/Skill-Rank-Steigerung ✅ FIXED

- **Datei:** src/gui/epwins.py (`__takeValsCat` L3210, `__takeValsSkill` L2937).
- **Status:** FIXED — Stand in Commit `63cad53` (hermes_dev).
- **Beschreibung:** DP wurde bei Rank-Steigerung weder abgezogen noch
  angezeigt. Ursache: `dpCosts`/`parent_dpCosts` im JSON als Listen
  (z. B. `[2,2,2]`), Code erwartete teils String (`.split(' ')`) →
  stummer `AttributeError` im Tkinter-Button-Callback.
  Abgedeckt über Typ-Guards (`ab23950`: `isinstance(..., str)`-Zweig,
  `type(dpCosts) == type(1)`-Zweig) + D1-Fix in `63cad53`
  (Reserved-Commit in `__closewin`), DP-Zeilen in `__finalize` aktiviert.
- **Verifiziert:** Xvfb-Harness `src/gui/test_dp_repro.py` — Cat:
  `__usedDP` 0→2, DPtext 79→77; Skill: 2→3, DPtext 77→76. EXIT=0.
  Analyse: `src/BUG_008_DP_DEDUCTION_ANALYSIS.md` (Abschnitt 9).
- **Offener Rest:** D3-Defekt (`__renameSkill`) wurde in BUG-016 behoben.

## [BUG-016] `__renameSkill` commit/restore-Tanz verliert `__usedDP` bei Exception (Defekt D3) ✅ FIXED

- **Datei:** src/gui/epwins.py (`__renameSkill` L3459).
- **Status:** FIXED — Stand in diesem Commit (hermes_dev).
- **Beschreibung:** `__renameSkill` zählte die Session-DP-Reservierung
  aus `__usedDP` ab und in `character['DP']` ein (L3459–3460) und
  stellte `character['DP']` am Ende manuell wieder her (L3492) — ohne
  try/finally. Bei Exception im Rebuild-Pfad (`__calcTotals`/
  `__buildWin`/`__buildTree`/`__buildChangedTree`) blieb die Reservierung
  dauerhaft in `character['DP']` eingebrannt und das Ledger leer →
  doppelter DP-Abzug beim späteren Finalize bzw. verlorenes Rename
  ohne Rollback. Zweitens: safe Lookup fehlte — ein KeyError auf
  `__changed['cat'][cat]` bei fehlender Category schlug nach
  Reservation-Abzug.
- **Fix:** Vor dem temporären Commit ist der Vor-Zustand gesichert
  (`origDP`, `pre_new`/`prev_entry`, `prev_old`); `try/except/finally`
  stellt bei Exception das Skill-Dict UND die Reservation wieder her und
  gibt die Reservierung in das `__usedDP`-Ledger zurück. Im Erfolgsfall
  bleibt die Reservation im Ledger, weil `__finalize` der einzige
  Commit-Punkt ist (konsistent zum D1-Modell). Zusätzlich: safe
  `.get()`-Lookup auf `__changed['cat']`.
- **Verifiziert:** Xvfb-Harness `src/gui/test_d3_rename.py` —
  FAIL-PATH (Rollback auf Exception), OK-PATH (Reservation im Ledger),
  FINALIZE (exakt `DP0 - RES` abgezogen). **ALL GREEN**.
  Regression: `src/gui/test_dp_repro.py` EXIT=0.
  Analyse: `src/BUG_008_DP_DEDUCTION_ANALYSIS.md` (Abschnitt D3).

## [BUG-017] `UnboundLocalError('lowval')` in `__takeValsSkill` bei bereits geaendeter Kategorie ✅ FIXED

- **Datei:** src/gui/epwins.py (`__takeValsSkill`, Ableitungsblock L2993ff).
- **Status:** FIXED — Stand in Commit `f67705b` (hermes_dev).
- **Beschreibung:** Skill-DP-Abzug war defekt, wenn ZUERST eine Kategorie
  geaendert (`__takeValsCat`) und danach ein Skill derselben Kategorie
  hochgestuft wurde — der normale GUI-Flow. Der
  "cat-bereits-in-__changed"-Zweig referenzierte `lowval`, das zuvor
  nur im "cat-noch-unveraendert + Skill-existiert"-Unterzweig
  zugewiesen wurde → `UnboundLocalError: cannot access local variable
  'lowval'`. Das Tkinter-Button-Callback stirbt still, also wird der
  Skill-Abzug nie gebucht — exakt das gemeldete Symptom "DP-Abzug fuer
  cat funktioniert, fuer skill nicht". Die bisherigen Harnesses
  deckten den Fall nicht ab, weil sie Cat + Skill in *verschiedenen*
  Kategorien kombinierten.
- **Fix:** `lowval` wird einmalig VOR der if/else-Logik aus
  `character['cat'][cat]['Skill'][skill]['lvlups']` abgeleitet
  (Fallback 0). Da `__changed['cat'][cat]` dieselbe Objekt-Referenz
  ist, stimmt die Ableitung in beiden Zweigen uberein; der
  "cat-bereits-veraendert"-Zweig ueberschreibt konsistent mit
  `__changed`, wie zuvor.
- **Verifiziert:** Neue Xvfb-Harness `src/gui/test_skill_after_cat.py`
  (cat + Skill in derselben Kategorie) — ohne Fix
  `UnboundLocalError('lowval')` (rot), mit Fix usedDP 0→2 (cat) → 4
  (skill), EXIT=0. Regression: `src/gui/test_dp_repro.py` EXIT=0;
  `test_d3_rename.py` ALL GREEN; `test_d1_close.py` OK.

## [BUG-018] `KeyError('Dwarves')` in `priorizeWeaponsWin.__setPPD` bei neuem Zwerg mit ungewähltem Realm ✅ FIXED

- **Datei:** src/gui/epwins.py (`priorizeWeaponsWin.__setPPD`).
- **Status:** FIXED — 2026-08-28, hermes_dev.
- **Beschreibung:** Neues Zwerg-Charakter mit noch ungewähltem Realm
  (`realm == 'choice'` — realms[0]) → `ppds[0] == ''` (leere String).
  Der Lookup `progressionType['' + 'Dwarves']` = `progressionType['Dwarves']`
  existiert nicht — in progressionType sind nur geprefixte Kombos wie
  `PPD Chan Dwarves`, `PPD Ess Dwarves`, `PPD Ment Dwarves` + `BD Dwarves`
  vorhanden → harter `KeyError: 'Dwarves'` im `__init__`/Char-Fluss.
- **Root Cause:** `ppds[0]` (choice) ist der Empty-String statt einer
  PPD-Präfix; der str-Zweig und der List-Zweig von `__setPPD` prüfen
  keinen Guard für leere/ppd-None Einträge.
- **Fix:** Beide Zweige (str- und list-typed `ppd`) werden per
  `if not entry or key not in progressionType: key = 'null'` abgesichert;
  Fallback = `progressionType['null']` = `(0, 0, 0, 0, 0)` (keine
  Progression, bis das Realm gewählt ist). Logger-Zeile bleibt im
  normalen Fall (keine Behavior-Änderung bei gültigen Realms).
- **Verifiziert:** Neue Harness `src/gui/test_choice_realm.py` — 3 Cases
  (realm='choice' → null-Fallback; realm='Channeling' → `PPD Chan Dwarves`;
  realm=['Channeling','Mentalism'] → max der beiden). Pre-fix: Case 1
  `KeyError: 'Dwarves'` (rot); post-fix: EXIT=0. Regressions:
  `test_d1_close.py`, `test_d3_rename.py`, `test_dp_repro.py`,
  `test_skill_after_cat.py` alle GREEN.

## [BUG-2248] `skillcatWin` — Charakterblatt "manchmal nicht abgespeichert" ✅ FIXED

- **Datei:** src/gui/epwins.py (`skillcatWin.__finalize` L3427ff, `__save` L3574ff).
- **Status:** FIXED — Stand in diesem Commit (hermes_dev).
- **Beschreibung:** Symptom "sometimes it does not store the character
  sheet successfully". Zwei Root Causes:
  - **A (KeyError im Commit-Pfad):** `__finalize` indizierte
    `self.__changed["cat"][cat]["rank"]` bzw. `["total bonus"]`
    ungezwungen für jede Kategorie in `__changed["cat"]`. Ein
    verwaister Legacy-/Rename-Eintrag ohne diese Keys löste den
    `KeyError` NACH der DP-Reservierung aus → Finalize brach ab,
    weder `.json` noch `.changes.json` entstand, das Fenster lief
    aber weiter wie ein Erfolg → "sporadisch nicht gespeichert".
  - **B (still loss in `__save`):** `__save` baute
    `spath/player/name+ending`, ohne das Zielverzeichnis
    `os.makedirs(..., exist_ok=True)` zu erzeugen. `writeJSON`
    (`rpgtoolbox/globaltools.py` L353) *swallowed* jeden IO-Fehler
    (`except Exception: logger.error`) → fehlendes Verzeichnis
    (`FileNotFoundError`) bedeutete Silent Data Loss; der
    Rest-Flow (`.changes.json`-Write, Fenster-Reset) lief auf.
- **Fix:** (A) defensive `.get()`-Kopien der zwei Werte statt
  ungezwungenen Indexes — ein fehlender Key wird übersprungen
  statt abzuwerfen. (B) `__save` sichert nun
  `os.makedirs(os.path.dirname(pathfile), exist_ok=True)` vor dem
  `writeJSON`-Call.
- **Verifiziert:** Neue Harness `src/gui/test_final_save.py` —
  Case A (KeyError-Sim) FAIL-PATH pre-fix, PASS post-fix;
  Case B (fehlendes Zielverzeichnis) — pre-fix: `FileNotFoundError`
  (silent, `.json` nicht da); post-fix: Verzeichnis wird erzeugt,
  `.json` liegt an Ort und Stelle, `.snap` ebenfalls (EXIT=0, 3/3).
  Regression: `test_choice_realm.py` (3/3), `test_dp_repro.py`
  (2/2), `test_skill_after_cat.py` (4/4), `test_d1_close.py`,
  `test_d3_rename.py` — alle GREEN.

## BEREITS GEFIXT - NICHT MEHR AKTUELL

| Bug | Status | Details |
|-----|--------|---------|
| BUG-001 | ✅ FIXED | foundherbs.py: None → [] |
| BUG-002 | ✅ FIXED | Image.LANCZOS → Image.Resampling.LANCZOS |
| BUG-003 | ✅ FIXED | Duplicate randint import entfernt |
| BUG-005 | ✅ FIXED | print(os.getcwd()) entfernt |
| BUG-006 | ✅ FIXED | Channeling/Leitmagie check korrekt |
| BUG-009 | ✅ GECHECKT | logger-Pfad in findherbs.py OK |
| BUG-010 | ✅ GECHECKT | 2026-08-28: Imports in treasure.py/charactertools.py headless getestet — relative/absolute Imports laufen ohne Fehler |
| BUG-011 | ✅ DUPLICAT | Duplicate of BUG-006 |

## TIEFERER AUDIT - GEFUNDENE MUSTER NACH BEHABUNGsort der vorherigen Manuellen Fixes

### 1. MUTABLE DEFAULT ARGUMENTS (47 Stellen auf 14 files)

Erzeugen geteilte Standardobjekte über alle Aufrufe hinweg. Daten werden beim zweiten Aufruf stillschweigend überschrieben.

| Datei | Zeile | Default | Risiko |
|-------|-------|---------|--------|
| attackcheck.py | 67 | `charlist = {}` | Shared dict |
| attackcheck.py | 760 | `mylist = []` | Shared list |
| monstercreator.py | 1043 | `GMtable = []` | Shared list |
| monstercreator.py | 1315 | `comparevalues = []` | Shared list |
| monstercreator.py | 1377 | `dictlist = []` | Shared list |
| monstercreator.py | 1788 | `comparevalues = []` | Shared list |
| monstercreator.py | 1879 | `CPtable = []` | Shared list |
| findherbs.py | 75 | `herbs = []` | Shared list |
| findherbs.py | 258 | `charlist = []` | Shared list |
| epcalcwin.py | 46 | `charlist = []` | Shared list |
| epcalcwin.py | 615 | `charlist = []` | Shared list |
| epcalcwin.py | 691 | `character = {}` | Shared dict |
| rm-inventory.py | 68 | `char = {}` | Shared dict |
| rm-inventory.py | 717 | `char = {}` | Shared dict |
| rm-inventory.py | 1977 | `char = {}` | Shared dict |
| rm-inventory.py | 3409 | `char = {}` | Shared dict |
| rm-inventory.py | 4981 | `purse = {}` | Shared dict |
| rm-inventory.py | 5023 | `worth = {}` | Shared dict |
| gui/winhelper.py | 38 | `opts = {}` | Shared dict |
| gui/winhelper.py | 87 | `opts = {}` | Shared dict |
| gui/gmtools.py | 252 | `charlist = []` | Shared list |
| gui/gmtools.py | 721 | `charlist = []` | Shared list |
| rpgtoolbox/chartotext.py | 105 | `data = {}` | Shared dict |
| rpgtoolbox/handlemagic.py | 42 | `charrealm = []` | Shared list |
| rpgtoolbox/handlemagic.py | 233 | `character = {}` | Shared dict |
| rpgtoolbox/globaltools.py | 48 | `dictlist = []` | Shared list |
| rpgtoolbox/globaltools.py | 177 | `file_list = []` | Shared list |
| rpgtoolbox/globaltools.py | 231 | `dic = {}` | Shared dict |
| rpgtoolbox/globaltools.py | 247 | `array = []` | Shared list |
| rpgtoolbox/globaltools.py | 273 | `array = []` | Shared list |
| rpgtoolbox/globaltools.py | 307 | `dic = {}` | Shared dict |
| rpgtoolbox/globaltools.py | 328 | `content = {}` | Shared dict |
| rpgtoolbox/globaltools.py | 498 | `chklist = []` | Shared list |
| rpgtoolbox/globaltools.py | 515 | `clist = []` | Shared list |
| rpgtoolbox/globaltools.py | 529 | `clist = []` | Shared list |
| rpgtoolbox/rrwindow.py | 46 | `charlist = []` | Shared list |
| rpgtoolbox/rolemaster.py | 1348 | `character = {}` | Shared dict |
| rpgtoolbox/rolemaster.py | 1385 | `purse = {}` | Shared dict |
| rpgtoolbox/rolemaster.py | 1463 | `char = {}` | Shared dict |
| rpgtoolbox/rpgtools.py | 78 | `charval = {}` | Shared dict |
| rpgtoolbox/rpgtools.py | 274 | `character = {}` | Shared dict |
| rpgtoolbox/combat.py | 59 | `cl = []` | Shared list |
| rpgtoolbox/combat.py | 165 | `achar = {}` | Shared dict |
| rpgtoolbox/combat.py | 258 | `cmbtlist = []` | Shared list |
| rpgtoolbox/combat.py | 347 | `comlist = []` | Shared list |
| rpgtoolbox/latexexport.py | 84 | `char = {}` | Shared dict |
| rpgtoolbox/latexexport.py | 495 | `character = {}` | Shared dict |
| rpgtoolbox/latexexport.py | 615 | `character = {}` | Shared dict |
| rpgtoolbox/rmfight.py | 79 | `data = {}` | Shared dict |
| rpgtoolbox/rmfight.py | 138 | `critresult = {}` | Shared dict |

**Fix Pattern:** `def foo(mylist=None, **kw): mylist = mylist or []`
**oder:** `def foo(mylist=None, **kw): mylist = list(mylist) if mylist is not None else []`

### 2. BARE EXCEPT (8 Stellen)

Fängt `SystemExit`, `KeyboardInterrupt`, `GeneratorExit` stillschweigend ab.

- `src/findherbs.py:582`
- `src/gui/gmtools.py:157`
- `src/gui/epwins.py:2170`
- `src/rpgtoolbox/globaltools.py:72`
- `src/rpgtoolbox/globaltools.py:356`
- `src/rpgtoolbox/treasure.py:97`
- `src/rpgtoolbox/treasure.py:100`
- `src/rpgtoolbox/treasure.py:127`

**Fix:** `except:` → `except Exception:`

### 3. `== True / == False / == None` (28 Stellen auf 7 files)

PEP 8 Style Issue — funktioniert auf CPython, ist aber bad practice und RuntimeWarning in manchen Kontexten.

| Datei | Zeilen | Muster |
|-------|--------|---------|
| gui/epwins.py | 91, 232, 251, 267, 1334, 1865, 2270, 2635, 2698, 3545, 3992, 4330, 4587 | `== None` / `!= None` |
| gui/winhelper.py | 57, 99, 184, 186 | `!= None` |
| gui/winhelper.py | 76 | `== True` |
| attackcheck.py | 1419 | `== None` |
| rpgtoolbox/globaltools.py | 101, 143 | `== None` |
| rpgtoolbox/confbox.py | 213, 366 | `== None` |

**Fix:** `is None` / `is not None` / nutze Truthiness (`if x:` statt `if x == True:`)

### 4. INVALID / LaTeX ESCAPE SEQUENCES in Non-Raw Strings (30+ files)

Python 3.12+ emittiert `SyntaxWarning` für Backslash-Sequenzen die keine gültigen Python-Escapes sind — meist beabsichtigte LaTeX-Marker (`\section`, `\pagebreak`, `\\author`, `\&`, etc.).

**Betroffene Dateien und Anzahl:**
| Datei | Escapes |
|-------|---------|
| rolemaster/encounters.py | 8 |
| rolemaster/specials.py | 8 |
| rolemaster/spellcasting.py | 12 |
| rpgToolDefinitions/csvdef.py | 7 |
| rpgToolDefinitions/epcalcdefs.py | 12 |
| rpgToolDefinitions/inventory.py | 7 |
| rpgToolDefinitions/magic.py | 8 |
| rpgToolDefinitions/middleearth.py | 7 |
| rpgtoolbox/calendar.py | 8 |
| rpgtoolbox/charactertools.py | 9 |
| rpgtoolbox/charhandler.py | 8 |
| rpgtoolbox/chartotext.py | 9 |
| rpgtoolbox/combat.py | 5 (`\n`, `\t`, LaTeX escape prefixes) |
| rpgtoolbox/confbox.py | 12 |
| rpgtoolbox/epcalc.py | 11 |
| rpgtoolbox/errbox.py | 9 |
| rpgtoolbox/globaltools.py | 10 |
| rpgtoolbox/handlemagic.py | 1 (`\n`) |
| rpgtoolbox/lang.py | 28 |
| rpgtoolbox/latexexport.py | 26 (`\begin`, `\caption`, `\chapter`, `\hline`, etc.) |
| rpgtoolbox/logbox.py | 8 |
| rpgtoolbox/merp.py | 7 |
| rpgtoolbox/rmfight.py | 9 |
| rpgtoolbox/rolemaster.py | 15 |
| rpgtoolbox/rpgtools.py | 1 (`\N` — tatsächlicher Python Escape, NICHT LaTeX) |
| rpgtoolbox/rrwindow.py | 1 |
| rpgtoolbox/treasure.py | 10 |

**Fix:** Strings mit `r"..."` Raw-String markieren oder Backslashes escapen: `"\\section"`

#### Special case: rpgtools.py:468
```python
logger.debug(f"result:\N...")  # Invalid — \N erwartet Unicode char name
```
**Fix:** `f"result:\\n<json>"` oder `r"result:\n<json>"`

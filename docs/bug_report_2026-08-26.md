# Bug-Report — rpg-tools (2026-08-26)

**Repo:** `/home/mongol/git/rpg-tools`  **Branch:** `hermes_dev`  **Commit-Referenz:** `1e6a7c7`
**Scope:** Alle `.py`-Dateien unter `src/` (Daten, JSON, pics, logs, `data/` sind ausgenommen).
**Methodik:**
1. `py_compile` auf alle Module → Syntax-Fehler.
2. AST-Heuristik (star-import-frei) → unbekannte Namen, Name-Mangling, doppelte Definitionen.
3. Jede Treffer **manuell** gegen den Code-Kontext verifiziert (kein False-Positive).
4. Smoke-Test `epcalcwin_gui.py`: `py_compile` OK + `xvfb-run /tmp/smoke_win.py` → EXIT 0 (PASS).

## Zusammenfassung

| Klasse | Anzahl | Status |
|--------|--------|--------|
| Live-Bug (crasht bei Aufruf) | **1** | **BEHOBEN** (2026-08-26, verifiziert) |
| Syntax-Bugs (Datei kompiliert nicht) | 3 | offen (nur Wartungs-Skripte) |
| False-Positives (ausgeschlossen) | 19+ | — |
| Bekannte Projekt-Konventionen (keine Bugs) | ~90 | — |
| Wartbarkeit (Doppel-Import) | 1 | offen (optional) |

## 1. Live-Bug — HOHE Schwere

### BUG-01 — `rpgtoolbox/edit_inv_core.py:65-70` — `NameError: item`

```python
def transport_item_to_container(character, gear_idx, container_name):
    gear = character.get('inventory', {}).get('gear', []) or []
    if gear_idx < 0 or gear_idx >= len(gear):
        return {'success': False, 'msg': 'Ungultiger Container-Index'}

    item['location'] = 'unequipped'          # <-- item NICHT definiert!
    item['container'] = container_name       # <-- item NICHT definiert!

    gear[gear_idx] = item                    # <-- undefined reference
    character['inventory']['gear'][gear_idx] = item
    calc_carried_weight(character)
    return {'success': True, 'placed_in': container_name}
```

**Ursache:** Die `item = dict(gear[gear_idx])`-Zuweisung (die in der Sibling-Funktion
`unpack_container_item()` auf L77 existiert) fehlt hier komplett → jede Aufruf
crasht mit `NameError: name 'item' is not defined`.

**Status:** BEHOBEN (2026-08-26) — fehlende Zeile `item = dict(gear[gear_idx])`
eingefügt; Live-Test: `transport_item_to_container(ch,0,'Backpack')` →
`{'success': True, 'placed_in': 'Backpack'}`, `location='unequipped'`, `container='Backpack'` ✓.

**Korrektur (nach Muster der Sibling-Funktion):**

```python
def transport_item_to_container(character, gear_idx, container_name):
    gear = character.get('inventory', {}).get('gear', []) or []
    if gear_idx < 0 or gear_idx >= len(gear):
        return {'success': False, 'msg': 'Ungultiger Container-Index'}

    item = dict(gear[gear_idx])           # <-- neu, nach L77-Pattern
    item['location'] = 'unequipped'
    item['container'] = container_name
    …
```

**Seit:** `deed06a` (initial commit des Refactor).


## 2. Syntax-Bugs (Dateien kompilieren NICHT)

### BUG-02 — `maintenance/final-tcheck.py:8` — IndentationError

```
7| print("=== TCHECK: Post-S1/S2/S3 ===\n")
8| # 1) Syntax-Checkmodules_to_check = [    "rpgtoolbox/combatcore.py",
9|     "gui/modules/attackcheck_gui.py" ,
```

Der Kommentar `# 1) Syntax-Check` und die Zuweisung `modules_to_check = [`
liegen auf **einer** Zeile verschmolzen → Python parst L9 als über-indizierte
Fortsetzung → `IndentationError: unexpected indent` bei `py_compile`.

**Korrektur:** Zeile 8 spalten in Kommentar + Zeile und `[` neu:
```python
# 1) Syntax-Check
modules_to_check = [
    "rpgtoolbox/combatcore.py",
    "gui/modules/attackcheck_gui.py" ,
```

### BUG-03 — `maintenance/s3_analyze.py:33` — SyntaxError

```python
elif current_method:            # L32, gehört zum äußeren if-Block
    buf.append(line)
                                # L32 leer
elif current_method:            # L33 — zweites elif ohne passendes if
    src = '\n'.join(buf)
    …
```

L33 `elif` steht **nach dem for-Loop** auf Spalte 0 — ein `elif` darf aber nur
direkt ein `if` folgen, davor liegt eine `for`-Anweisung → `SyntaxError`.
Daran anschließt sich ein zweiter Defekt: das innere `elif current_method:` (L30)
gehört eigentlich als elif-Flügel des inneren `if m:` auf L22 (dort sollte `buf.append(line)`
stehen) — dadurch werden bei korrekter Ausführung nie die Methoden-Körperzeilen
gesammelt. Ursprung: kaputte Indentation beim manuellen Edit/Refactor.

### BUG-04 — `maintenance/s3_c_split.py:10/18` — NameError: `ranges`

```python
10| rances = [                    # L10: Variable heißt 'ranches' (Typo)
11|     ("win", 62, 723),       # InventoryWin
12|     ("shop", 724, 1983),    # shopWin
13|     ("enchant", 1984, 3415),# enchantItem
14|     ("edit", 3416, 5068),   # editinventory (letzte Klasse)
15| ]
17| for name, start, end in ranges:     # L18: 'ranges' ist undefiniert
```

Typo `ranches` vs. `ranges` → `NameError: name 'ranges' is not defined`.

**Korrektur:** L10 `ranches` → `ranges`.

Alle drei Dateien sind **einmalige Wartungs-Skripte** aus dem Refactor —
sie werden im normalen App-Pfad nicht geladen, haben aber den
`py_compile`-Check der Repo-Suite gescheitert.


## 3. False-Positives (verifiziert, NICHT Bug)

| Datei:Zeile | Treffer | Begründung |
|-------------|---------|------------|
| `rpgtoolbox/calendar.py:112` | `weekdaynamess['Shire']`, `monthnames['Shire']` | Beide Modul-Globale vorhanden (L21, L89), Key `'Shire'` in beiden vorhanden. |
| `rpgtoolbox/rolemaster.py:1396` | `dice` | Lokale `from rpgtoolbox.rpgtools import dice` auf L1395 direkt vor der Nutzung. |
| `rpgtoolbox/globaltools.py:82,369` | `logger`, `error` | `logger` modul-global (L45); `error` ist Binder in `except … as error:` (L367). |
| `rpgtoolbox/herbalogic.py:52` | `logger` | Modul-global (L17). |
| `rpgtoolbox/logbox.py:64,79` | `LEVEL`, `MB`, `KB`, `GB` | Alle Modul-Globale (L23-34). |
| `rpgToolDefinitions/csvdef.py:38` | `initialHeaders` | Modul-global (L17). |
| `rpgToolDefinitions/middleearth.py:102` | `areas` | Modul-global + lokale `global areas`-Deklaration (L97). |
| `rpgtoolbox/enchant_core.py:8` | `BONUS_MULT` | Modul-global (L5). |
| `gui/modules/epcalcwin_gui.py` 83/89/95, 1206, 1270, 1273 | `self.__open`, `self.__save`, `self.__quit`, `self.t`, `self.c` | Alle in `EPCalcWin.__init__`/`__winCasting` definiert – korrekte Name-Mangling, AST-bestätigt. |
| ~90× `SyntaxWarning: invalid escape sequence` | `\p`, `\e`, `\d`, `\l`, `\h`, `\_`, `\%`, `\&`, `\c` | Beabsichtigte Doxygen-Inlinedoku-Konvention des Projekts (siehe `magic.py`, `csvdef.py` u. a.). Pythons String-Parser warnt, die Bedeutung bleibt erhalten. |
| `gui/modules/inventory_gui.py:50,56` | Doppelte `edit_inv_core`-Import | Gleiche Symbol-Liste, kein Name-Konflikt — Wartbarkeit, keine Logik-Bug. |

## 4. Verifikation

- `py_compile` auf allen 21 sauberen .py-Dateien: **OK** (21/21)
- `epcalcwin_gui.py` Smoke-Test unter xvfb: **EXIT 0** — `EPCalcWin`-Init, `__open`, `__winCasting` (Toplevel + Listen + Spellen gebaut) und Aufräumen, alles OK
- `epcalcwin.py` unter xvfb-Run: mainloop läuft (Timeout 12 s = korrekt), kein `AttributeError` mehr
- AST: 24 Methoden in `EPCalcWin`, alle Name-Mangling-Referenzen (L83, L89, L95) auf definierte Methoden

## 5. Empfehlung

1. **BUG-01 — BEHOBEN** (2026-08-26): `item = dict(gear[gear_idx])` eingefügt, Live-Test bestanden.
2. **BUG-02/03/04** (maintenance-Skripte): je 1-2 Zeilen Fix, oder die Dateien archivieren, wenn sie keine Relevanz mehr haben.
3. Optional: `inventory_gui.py` L50 und L56 zusammenführen (Doppel-Import).
4. Optional: `\p`-Doxygen-Doku durch `r'''…'''`-Raw-Strings in neuem Code vermeiden, um die ~90 SyntaxWarnings zu reduzieren. Bestehende bleiben (bekannte Projekt-Konvention).

*Erstellt: 2026-08-26 · Autor: Hermes Agent · Repo: `hermes_dev` @ `1e6a7c7`*

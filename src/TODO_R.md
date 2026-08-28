# TODO_R — Wiederherstellung nach Modularisierungs-Break (2026-08-18/19)

## Lage-Bild (kurz)

Zwei Commits auf `hermes_dev` haben die 6 Launcher-Dateien kaputtgemacht:

| Commit | Schaden |
|---|---|
| `c2f6531` "Bugfixes & Documentation Consolidation" | `attackcheck.py` (Kampftool `atWin` + `enemySelector` + `calFightEP`, ~2750 Zeilen) wurde durch MonsterCreator-Inhalt ersetzt. `atWin` ist damit aus dem Arbeitsbaum verschwunden. |
| `30e1e8a` "hermes hat das unheil angerichtet" | Alle 6 Starter-Dateien (`attackcheck.py`, `epcalcwin.py`, `findherbs.py`, `monstercreator.py`, `rm-inventory.py`, `rm_char_tools.py`) wurden zu Import-Shims reduziert. Alle `if __main__ == '__main__':`-Blöcke weg — `python <datei>.py` startet nichts mehr. |

**Recover-Basis:** Commit `b30b498` (letzter gesunder Stand, inkl. BUGS-Fixes bis BUG-001).
`master` = älter (vor BUGS-Fixes), `a12aeda` = attackcheck.py schon kaputt, `origin/attackwin` = atWin vorhanden (alternativ).

### Konkrete Schadensliste (verifiziert)

1. **atWin-Kampfsimulator LIEGT KEINWOHL MEHR IM ARBEITSBaum** — `attackcheck.py` importiert nur noch MonsterCreator-Klassen (`gui/modules/attackcheck_gui.py`). `atWin`, `enemySelector`, `calFightEP` existieren nur noch in der Git-Historie.
2. **`gui/modules/inventory_gui.py` Zeile 4717:** Modulebene `win = InventoryWin()` — Fenster öffnet sich BEIM IMPORT (Side-Effect!). Ohne `$DISPLAY` crasht sogar `import gui.modules.inventory_gui` (verifiziert). Auch `rm-inventory.py`-Shim ist davon betroffen.
3. **`gui/monstercreator.py` (88 Zeilen):** Halb-fertiges Skelett mit inkompletten Klassen (`monstercreatorWin.__init__` bricht mit Kommentar "# ... rest of __init__ ..." ab). Von niemandem importiert — aber Falle für künftige Imports.
4. **6 Launcher ohne `__main__`-Block:** `attackcheck.py`, `epcalcwin.py`, `findherbs.py`, `rm-inventory.py`, `rm_char_tools.py` (+ `monstercreator.py` als zweites MonsterCreator-Duplikat).
5. **Orphane Duplikat-Module** (von s3_split.py generiert, von NIEMANDEM importiert):
   - `gui/modules/inv_win.py` (662 Z.), `inv_shop.py` (1260 Z.), `inv_enchant.py` (1432 Z.), `inv_edit.py` (1653 Z.)
   - `gui/modules/editinventory_core.py`, `enchantitem_core.py`, `shopwin_core.py`, `inventorywin_core.py` (~4500 Z. gesamt)
   - `gui/modules/inv_separate/` — nur noch `__pycache__`, keine .py mehr
   - `string2worth` definiert drettfach: `rpgtoolbox/herbalogic.py`, `inventory_gui.py`, `inv_edit.py`/`editinventory_core.py`.
   - **NICHT** orphan: `rpgtoolbox/combatcore.py`, `shop_logic.py`, `enchant_core.py`, `edit_inv_core.py`, `herbalogic.py` — diese werden aktiv importiert.
6. **Einmal-Skripte liegen lose in `src/`:** `s3_analyze.py`, `s3_split.py`, `s3_c_split.py`, `s3_core_extractor.py`, `split_attack_gui.py`, `fix_dups.py`, `fix_s1_attackcheck.py`, `fix_s1_write_all.py`, `final-tcheck.py`.

### Was IST ok (nicht anfasst!)

- `gui/modules/attackcheck_gui.py` (MonsterCreator-Klassen komplett + `__main__`) ✓
- `gui/modules/epcalcwin_gui.py` (EPCalcWin/showGrpEP/manWin + `__main__`) ✓
- `gui/modules/findherbs_gui.py` (searchHerbsWin + `__main__`) ✓
- `gui/modules/char_tools_gui.py` (MainWindow-Import + `__main__`) ✓
- `rpgtoolbox/combat.py`, `rmfight.py`, `rolemaster/*`, `gui/epwins.py` (MainWindow) ✓
- `rpgtoolbox/*_core.py`, `combatcore.py`, `herbalogic.py` als Logik-Module ✓

---

## TODOs

### [TR-001] atWin-Kampftool wiederherstellen — HÖCHSTE PRIORITÄT
- **Verloren:** `calFightEP`, `atWin` (~2650 Zeilen), `enemySelector` — in `gui/` und `src/` nirgends mehr vorhanden.
- **Quelle:** `git show b30b498:src/attackcheck.py` (vollständig, inkl. `savePartyStatus` und BUGS-Fixes).
- **Plan:**
  1. atWin/enemySelector/calFightEP aus `b30b498` in neues Modul `gui/modules/attackwin_gui.py` überführen (GUI-Hälfte, mit `__main__`-Block `win = atWin()`).
  2. `attackcheck.py`-Shim neu schreiben: `from gui.modules.attackwin_gui import atWin, enemySelector, calFightEP` + `__main__`: `win = atWin()`.
  3. Dependencies prüfen: `rpgtoolbox.combat`, `rolemaster.specials`, `handlemagic` → alle existieren im aktuellen Baum, Diff zu `b30b498` minimal.
  4. **NICHT** `a12aeda` als Basis nehmen (attackcheck.py ist dort schon MonsterCreator-Content).
- **Risiko:** `atWin`-Code greift auf `rpgtoolbox.combat.*` zu, das seit `b30b498` um 19 Zeilen geändert wurde → Import-Test + Smoke-Test Pflicht.

### [TR-002] `inventory_gui.py` Side-Effect entfernen — HÖCHSTE PRIORITÄT ✅ GESCHLOSSEN
- **Verifiziert 2026-08-28:** `rm-inventory.py` importiert headless (ohne DISPLAY) OHNE
  Side-Effect-Crash; Xvfb-Smoke-Test läuft (Fenster öffnet sich).
- **Problem:** Zeile 4717 steht nacktes `win = InventoryWin()`. Jede importierende Datei öffnet das Fenster bzw. crasht ohne DISPLAY (verifizierter Crash).
- **Plan:**
  1. Zeile 4717 (Leererzeile + `win = InventoryWin()`) aus `gui/modules/inventory_gui.py` löschen.
  2. Stattdessen sauberen `if __name__ == '__main__': win = InventoryWin()`-Block anhängen.
  3. `rm-inventory.py`-Shim: `__main__`-Block ergänzen (`win = InventoryWin()` nach `chkCfg()`-Aufruf wie im Original `b30b498:src/rm-inventory.py`; original hatte KEINEN `__main__`-Block, sondern genau diese Side-Effect-Zeile — also Intent = Fenster beim Start).

### [TR-003] Launcher-`__main__`-Blöcke in den 5 Shims wiederherstellen — HOHE PRIORITÄT
- `epcalcwin.py`: `__main__` aus `epcalcwin_gui.py` (L1017ff) spiegeln oder nur `from gui.modules.epcalcwin_gui import EPCalcWin` + `win = EPCalcWin()` (Achtung: Original-`__main__` liest `charparty.json` per HARDCODED Pfad — besser aus `mycnf` bauen).
- `findherbs.py`: `__main__` ergänzen: `win = searchHerbsWin()`.
- `rm_char_tools.py`: `__main__` ergänzen: Original-Block aus `b30b498:src/rm_char_tools.py` kopieren (chkCfg → Logger → `MainWindow(lang, title="EP Calculator", storepath)` → "Program finished").
- `attackcheck.py`: s. TR-001.
- `monstercreator.py`: bereits funktional (Shim auf attackcheck_gui); nur semantisch prüfen, ob Klassen-Zuordnung ok ist (siehe TR-004).

### [TR-004] MonsterCreator-Duplikate entscheiden — HOHE PRIORITÄT
- **Ist-Zustand:** MonsterCreator-Klassen sitzen in `gui/modules/attackcheck_gui.py` (komplett, funktional); `gui/monstercreator.py` ist ein 88-Zeilen-SKELETT mit unvollständigen Klassen; `attackcheck.py` UND `monstercreator.py` sind beide Shims auf dieselben Klassen.
- **Entscheidung (eins der beiden):**
  a) Klassen in `gui/monstercreator.py` (kanonische Position!) verschieben, `attackcheck_gui.py` als Abwärtskompat-Import-Schicht lassen, `gui/monstercreator.py`-Skelett ALLES überschreiben. **← Empfehlung**
  b) Alles in `attackcheck_gui.py` belassen, `gui/monstercreator.py`-Skelett löschen.
- **Aktion nach Entscheidung:** Skelett `gui/monstercreator.py` entfernen/überschreiben (Falle!), `attackcheck.py` auf TR-001-Basis neu bauen.

### [TR-005] Orphane-Duplikat-Module aufräumen — MITTELRE PRIORITÄT
- **Entscheidung:** `inventory_gui.py` (4717 Z.) ist der kanonische Standort (wird von `rm-inventory.py` importiert). Dann löschen:
  - `gui/modules/inv_win.py`, `inv_shop.py`, `inv_enchant.py`, `inv_edit.py`
  - `gui/modules/editinventory_core.py`, `enchantitem_core.py`, `shopwin_core.py`, `inventorywin_core.py`
  - `gui/modules/inv_separate/` (nur `__pycache__`)
- **ABER VOR LÖSCHEN:** `git diff` je Datei gegen die entsprechende Klasse in `inventory_gui.py` prüfen, ob Split-Files neuere Fixes enthalten (sie stammen aus s3_split.py, Stand Aug 13). Falls ja: erst in `inventory_gui.py` mergen, dann löschen.
- ALTERNATIV: Umgekehrt (auf Split-Files aufbauen, `inventory_gui.py` ablösen) — nur wenn Diff zeigt, dass Split-Files deutlich aktueller sind.

### [TR-006] `string2worth`-Tripelpflege konsolidieren — MITTELRE PRIORITÄT
- `herbalogic.py` (Kraut-Wertung), `inventory_gui.py` L4699, `inv_edit.py`/`editinventory_core.py` (wird mit TR-005 ggf. aufgelöst).
- **Plan:** Nach TR-005 prüfen, ob `inventory_gui.py`-Version und `herbalogic`-Version identisch sind. Falls ja: `inventory_gui.py` importiert von `herbalogic` (wie `findherbs.py` schon macht). Falls Logik-Unterschiede: bewusst dokumentieren oder zusammenführen.

### [TR-007] Einmal-Skripte aus `src/` entfernen — NIEDRIGE PRIORITÄT
- `s3_analyze.py`, `s3_split.py`, `s3_c_split.py`, `s3_core_extractor.py`, `split_attack_gui.py`, `fix_dups.py`, `fix_s1_attackcheck.py`, `fix_s1_write_all.py`, `final-tcheck.py`
- **Plan:** in `src/maintenance/` verschieben (oder nach TR-005 komplett auflösen, wenn keine weiteren Split-Schritte mehr geplant sind).

### [TR-008] Verifikation (ABSCHLUSSGATE) — HÖCHSTE PRIORITÄT ✅ GESCHLOSSEN
**Abgeschlossen 2026-08-28:** 1. py_compile 70/70 ok. 2. Import-Test 5/5 Shims ok (headless, kein Crash). 3. `rm-inventory.py` headless ok. 4. Xvfb-Smoke: alle 6 Launcher ok (8s-Fensterlauf, SIGTERM). 5. atWin-Diff gegen b30b498: nur 4 Zeilen Kommentare/leer (TR-003/TR-004-Hinweise), keine Logikänderung. 6. `git status` sauber.
1. `python -m py_compile` über ALLE `.py`-Dateien in `src/` (keine Syntaxfehler).
2. Import-Test (headless, ohne DISPLAY): `import gui.modules.<each>` muss OHNE Fenster-Eröffnung und OHNE Crash gehen — Side-Effects sind erst ab TR-002 beseitigt, danach muss dieser Test grün werden.
3. `python -c "import attackcheck, epcalcwin, findherbs, monstercreator, rm_char_tools, rm_inventory"` — alle 6 Shims importierbar, keine Tk-Instantierung (rm-inventory = nur nach TR-002!).
4. Launcher-Smoke-Test unter Xvfb (`xvfb-run -a`): je 2s Runnzeit pro `python <launcher>.py`, expecting "Fenster erzeugt sich" (Tk init ok), dann SIGTERM.
5. Vergleichs-`diff -b` der restaurierten `atWin`-Klassen gegen `git show b30b498:src/attackcheck.py` (nur Verschiebung, keine Logikänderung!).
6. `git status` — ungetrackte Daten-Ordner (`data/Isdan.json` etc.) nicht anrühren!

---

## Reihenfolge (empfohlen)

```
TR-002 (Side-Effect beseitigen)   ← erst, weil TR-008-Import-Test ohne das Scheitern wird
TR-001 + TR-003 (atWin + Launcher-Shims)
TR-004 (MonsterCreator-Entscheidung)
TR-005 + TR-006 (Duplikate aufräumen + string2worth)
TR-007 (Skripte verschieben)
TR-008 (Verifikation)
```

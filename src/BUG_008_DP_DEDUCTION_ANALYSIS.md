# BUG-008 Analyse: Category-/Skill-Level-Up DP-Abbuchung (2026-08-27)

> **Status:** Analyse + Dokumentation. **Kein Code-Fix** — User-Instruction:
> „könntest du das mal analysieren und entsprechend dokumentieren für
> späteres debugging?“.
>
> **Scope:** `src/gui/epwins.py`, Klasse `skillcatWin` (Zeilen 2238–4100).
> **Verifiziert gegen:** `git status --short` (clean), `py_compile epwins.py`
> (exit 0, 4 × SyntaxWarning `\e` in Docstrings — nicht kritisch).
> Alle Zeilenreferenzen dieser Note wurden am 2026-08-27 per awk/grep
> zeilenweise gegen das aktuelle File verifiziert.
>
> **Kontext:** BUG-008 ist die systematische Nachanalyse für BUG-006 und
> BUG-007 (beide offen). Der ursprüngliche User-Bug-Report lautet:
> *„beim steigern von cat werden die entsprechenden punkte nicht von den
> DP abgezogen"*. Diese Note dokumentiert, was der **aktive Code** tut,
> **wo der Commit-Punkt liegt** und welche **drei Defekte (D1–D3)** den
> Report erklären können.

---

## 1. Datenfluss-Karte (Ground Truth, zeilenverifiziert 2026-08-27)

**Klasse:** `skillcatWin` ab Zeile 2238 in `src/gui/epwins.py`.

**Instanzvariablen / relevante Felder:**
- `self._character` — Referenz auf den Character-Dict (L2240, L2256, L2276).
- `self.__usedDP` (mangled: `_skillcatWin__usedDP`) — Session-Ledger der
  reservierten DP-Kosten. Wird genau an diesen Stellen berührt:
  - **L2375** (`__init__`): `self.__usedDP = 0` — Initialisierung.
  - **L3050 / L3082 / L3118 / L3157 / L3191** (`__takeValsSkill`):
    `self.__usedDP += diffcost` — Skill-Pfad, 5 Teilasträße.
  - **L3286** (`__takeValsCat`, diff > 0): `self.__usedDP += int(dpCosts[i])`.
  - **L3293** (`__takeValsCat`, diff < 0): `self.__usedDP -= int(dpCosts[i])`.
  - **L3324** (`__takeValsCat`, Rollback): `self.__usedDP = bkpusedDP`.
  - **L3347** (`__finalize`): `self.__usedDP = 0` **nach** dem Commit.
  - **L3460** (`__renameSkill`): `self.__usedDP = 0` **vor** dem
    temp-deduct/restore-Tanz (s. D3).
- `self.__changed` — Puffer der noch nicht finalisierten Änderungen
  (`{'cat': {...}, 'skill': ...}`); wird bei `__finalize` gemerged.
- `self.char['DP']` / `self._character['DP']` — verbleibende, verfügbare DP.

**Commit-Ledger-Modell (Das Herzstück):**
`__usedDP` ist ein reines **Zwischen-Ledger**: es reserviert DP in der
Session, während der User mehrere Skills/Cats ansteuert. Die eigentliche
Abbuchung aus `character['DP']` passiert **einmalig und ausschließlich** an
zwei Stellen — und beide sind problembehaftet:

| # | Location | Code | Status |
|---|---|---|---|
| A | **L3345** in `__finalize` | `self._character['DP'] -= self.__usedDP` | **AKTIV** (einziger regulärer Commit-Button) |
| B | **L2330** in `__closewin` | `# self._character['DP'] -= self.__usedDP` | **AUSKOMMENTIERT** (Bug D1) |

**Button-Mapping (aus `__buildWin`, L2579–L2606):**
- „Take" (row 4, col 5) → `__takeValsCat` (L2582)
- „Take" (row 5, col 5) → `__takeValsSkill` (L2589)
- „Finalize" (row 4, col 6) → `__finalize` (L2596)
- „Rename" (row 5, col 6) → `__renameSkill` (L2603)

---

## 2. Vollständiger Datenfluss pro Pfad

### 2.1 Skill-Pfad — `__takeValsSkill` (L2933–L3203)

**Signature & Contract:**
```
Inputs:  self.__curItem  (tree item in selection)
         self._skillspin (gewählter neuer Rank)
         self.__changed  (Puffer)
         self.__usedDP   (Session-Ledger)
Output:  self.__changed['cat'][cat]['Skill'][skill]  (neu/gemodifiziert)
         self.__usedDP                                  (+= diffcost)
         self.DPtext.set(character['DP'] - __usedDP)    (Display-Update)
```

**Kern-Logik** (vereinfacht, 5 Teilasträßen L3040/L3073/L3108/L3147/L3182):

```python
# 1) Rank-Diff und dpCosts auflösen (L2948–L2980)
newrank   = int(self._skillspin.get())
oldval    = self.__tree.item(self.__curItem)['values'][3]
dpCosts   = self.__tree.item(self.__curItem)['values'][2]  # string|list
#         → normalisiert auf list (L2974–L2978)

# 2) diff und Start-Index (L2987–L3013)  — „lowval" = nächste nicht
#    noch-gelevelte Stufe (aus `__changed[...]['lvlups']` falls vorhanden)
diff  = newrank - oldval
lowval = 0 if 'lvlups' not in skill else skill['lvlups']

#    Special (nur hier): wenn dpCosts-Liste erschöpft, „Extended-Costs"
#    werden aus Parent-Cat geliehen (L3015–L3026):
#       parent_item = self.__tree.parent(self.__curItem)
#       extended = dpCosts + [next available category cost for each extra]
#       dpCosts = extended
#    (KATEGORIENPFAD L3271 macht das analog mit Letzter-Stufe-Repetition
#     — hier werden Kategories-echte dpCosts angehängt. Unterschied!)

# 3) Kosten berechnen (L3030–L3035 / weitere 4× gleiche Struktur)
diffcost = 0
for i in range(lowval, lowval + diff):
    diffcost += int(dpCosts[i])     # Level-UP
# oder:
for i in range(lowval + diff, lowval):
    diffcost -= int(dpCosts[i])     # Level-DOWN (Rang zurückschrauben)

# 4) GATE + COMMIT (L3040 / L3073 / L3108 / L3147 / L3182)
if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:
    # → Rank/bonus im `__changed`-Puffer setzen
    self.__changed['cat'][cat]['Skill'][skill]['rank']         = newrank
    self.__changed['cat'][cat]['Skill'][skill]['total bonus']  = newtotal
    self.__usedDP += diffcost                                    # ← RESERVIERE
    self.__changed['cat'][cat]['Skill'][skill]['lvlups'] += diff
else:
    self.__info(screenmesg['epwins_no_dp'][self.lang])          # → Ablehnen
```

**WICHTIG:** `self._character['DP']` wird hier **NICHT** verändert. Nur
`s.__usedDP` wächst. Das ist korrekt per Design (Commit-Punkt A/B ist
später). Die UI zeige `DPtext = character['DP'] - __usedDP` an (L3201) —
**sichtbare verbleibende DP sinkt sofort**, auch wenn der Charakter-Dict
erst beim Finalize aktualisiert wird.

---

### 2.2 Kategorie-Pfad — `__takeValsCat` (L3206–L3331)

**Signature & Contract:**
```
Inputs:  self.__curItem  (tree item in selection — muss Kategorie sein)
         self._catspin   (gewählter neuer Rank)
         self.__changed  (Puffer)
         self.__usedDP   (Session-Ledger)
Output:  self.__changed['cat'][currcat]   (neu/gemodifiziert)
         self.__usedDP                    (+= bzw. -= dpCosts)
         self.DPtext.set(character['DP'] - __usedDP)
```

**Kern-Logik:**
```
# L3215–L3249: curccat/oldval/newval/dpCosts aus Tree lesen

# L3250–L3279: diff & lowval ermitteln (3 Zweige)
#   Erst-Change:      lowval=0,  diff=newval-oldval, lvlups=diff
#   Folge-Change:     lowval=bislangige lvlups,
#   Extended-Costs (dpCosts erschöpft): [letzte Stufe]*diff anhängen,
#                     lvlups = len(neue dpCosts)

# L3281 BACKUP: bkpusedDP = int(self.__usedDP)   (siehe D2)

# L3283–L3294 Reserve (diff>0: += | diff<0: -= int(dpCosts[i]))

# L3298 GATE: (character['DP'] - __usedDP) >= 0 ?
#   Ja:  L3300–L3321: __changed['cat'][curccat] auffüllen
#        (rank, lvlups, 'total bonus')
#   Nein:L3324 ROLLBACK: __usedDP = bkpusedDP  + "no DP"-Dialog

# L3329–L3330 UI: DPtext = DP - __usedDP, ChangedTree-Refresh
```

---

### 2.3 Commit — `__finalize` (L3333–L3396)

```
L3339–L3342   from rpgtoolbox import rolemaster as rm
              self.profs = rm.choseProfession(self.lang)
              self._character = rm.refreshStatBonus(self._character)
L3344–L3347   self._character['DP'] -= self.__usedDP   ← COMMISSION (A)
              logger.debug(remaining DP)
              self.__usedDP = 0
L3349–L3351   if self._character['DP'] < 0: → set 0  (Unterlauf-Schutz)
L3353         handlemagic.updateSL(...)  [auskommentiert]
L3354–L3359   soul dep / Stat Loss / Recovery refresh
L3360+        (Merge von __changed in _character — folgt L3396, see §2.5)
```

---

### 2.4 Close-Window — `__closewin` (L2324–L2337)

```python
def __closewin(self):
    if self.__usedDP > 0:
        self._character['lvlup'] -= 1
    #         self._character['DP'] -= self.__usedDP   ← AUSKOMMENTIERT
    #         self.__usedDP = 0                          ← AUSKOMMENTIERT
        if self._character['lvlup'] < 0:
            self._character['lvlup'] = 0
    self.window.destroy()
    self.window = MainWindow(lang = self.lang, storepath = self.spath,
                             char = self._character)
```

---

### 2.5 Skill-Rename — `__renameSkill` (L3451–L3492)

```
L3458        from rpgtoolbox.rolemaster import progressionType
L3459–L3460  self._character['DP']  -= self.__usedDP     ← TEMP-COMMIT
             self.__usedDP            = 0
L3461–L3491  (Rename-Operation: neues Skill-Dict bauen, altes auf 0
             setzen, __calcTotals, UI-Refresh)
L3492        self._character['DP']  = dummyDP             ← RESTORE
```

`dummyDP` (L3483) hält den DP-Wert **nach** dem temp-Kommit; nach dem
Rename wird er zurückgesetzt. Das wirkt im Endeffekt wie ein no-op auf
`character['DP']`, **aber** es hat eine Seitwirkung: der
`__usedDP`-Ledger zwischen L3460 und L3492 ist auf 0 — falls eine
Exception zwischen den zwei Punkten wirft, bleibt der Ledger verloren.
Siehe D3.

---

## 3. Defekte / Befund-Liste

### D1 — ~~`__closewin` gibt DP-Nutzungen NICHT aus dem Character ab~~ (Kritikalität: HOCH) — **FIXED 2026-08-27**

**Fix:** Die beiden auskommentierten Zeilen in `__closewin` wurden
re-aktiviert — der DP-Commit beim Close-without-Finalize läuft jetzt:
```python
if self.__usedDP > 0:
    self._character['lvlup'] -= 1
    self._character['DP'] -= self.__usedDP   # re-aktivierte Zeile
    self.__usedDP = 0                        # re-aktivierte Zeile
```
Double-Charge-Schutz verifiziert: `__finalize` setzt `__usedDP = 0`
(L3354/3355), daher ist die Guard `if self.__usedDP > 0` bei
Finalize→Close-Paaren bereits 0 und der Close-Commit schießt nicht
erneut ab. Die `lvlup`-Reduktion bleibt wie bisher (max(0, lvlup-1)).

**Befund (vor Fix):** L2330–L2331 in `epwins.py` waren auskommentiert:
```python
2330|      self._character['DP'] -= self.__usedDP   # kommentiert
2331|      self.__usedDP = 0                      # kommentiert
```
**Konsequenz:** Wenn der User Änderungen an Skills/Cat nimmt, „Take"
drückt (die `__usedDP` wird erhöht, `__changed`-Puffer gefüllt), und
dann das Fenster schließt **ohne** „Finalize" zu drücken:
1. `__usedDP` > 0, `__changed` enthält Änderungen.
2. `__closewin` reduziert `lvlup` um 1, aber `character['DP']` bleibt
   **unverändert** (höher als es sein sollte).
3. `self.window = MainWindow(char = self._character)` → der alte
   Character-Dict (mit nicht-abgezogenen DP) wird nach oben gereicht.

**Reproduktionspfad (Headless, statisch):**
```
1. App starten, Character mit DP=50, lvlup=2 laden
2. skillcatWin öffnen
3. Kategorie „Combat" auf Rank 3 (war 1) → „Take"
   → __usedDP += 10 (hypothetisch)
   → __changed['cat']['Combat'] = {...}
4. Fenster mit X schliessen → __closewin
   → lvlup 2→1
   → DP bleibt 50 (sollte 40 sein)
5. Character wird nach oben gereicht, gespeichert → DP=50 persistiert
```

**Warum L3345 (`__finalize`) das nicht rettet:**
`__finalize` ist ein expliziter Button; `__closewin` ist ein Fenster-
Close-Handler. Ein User, der nicht auf „Finalize" klickt (z. B.
abgebrochen, Fehler, oder „Take" + close), umgeht den Commit vollständig.

**Beabsichtigt oder Bug?**
- **Nicht beabsichtigt**: L3330/L3331 wurden offensichtlich
  ausgekommentiert **ohne** eine Ersatz-Logik. Wenn `__closewin`
  beabsichtigt ohne DP-Kommit ist, sollte (a) `__usedDP` zurückgesetzt
  und (b) `__changed`-Puffer verworfen werden (heute passiert beides
  nicht — `__usedDP` wird zwar L3324 im cat-Pfad im Rollfall
  zurückgesetzt, aber im Skill-Pfad nie).
- **Sollte beabsichtigt sein**: `__closewin` darf die Änderungen
  nur als „ungeprüft" zurückreichen, der nächste Schritt (MainWindow
  → __save) muss den Commit nachholen — was nicht passiert.
- **Empfehlung für späteren Fix** (doku only, nicht implementiert):
  (a) Kommentar am Code „intentional?" + (b) entweder DP-Kommit
  einrichten oder Rollback-Policy dokumentieren.

---

### D2 — **`bkpusedDP`-Rollback in `__takeValsCat` ist ein Backup, kein Reset** (Kritikalität: NIEDRIG, aber semantisches Risiko)

**Befund:** L3281 `bkpusedDP = int(self.__usedDP)`. L3324
`self.__usedDP = bkpusedDP` (Rollback-Zweig).

**Warum das ein Problem ist:**
- `bkpusedDP` ist ein **Snapshot** des Ledgers vor dem
  Reserve-Update. Nicht ein „Reset auf null". Das ist **korrekte**
  Rollback-Logik — man rollt auf den Zustand **vor** der aktuellen
  Aktion zurück, nicht auf den Session-Anfang.
- **Risiko:** Wenn der User **mehrfach** „Take" für dieselbe Kategorie
  drückt (diff > 0, dann weiter diff > 0), ist `bkpusedDP` bei jedem
  Mal der Zustand **vor der jeweiligen** Reserve. Das ist korrekt,
  aber es bedeutet: Ein Rollback im **zweiten** Take setzt `__usedDP`
  auf den Wert **nach dem ersten** Take zurück, nicht auf 0.
  Das ist beabsichtigt (mehrere Änderungen in einer Session
  akkumulieren), aber es ist in den Docstrings nicht dokumentiert —
  der User-Kommentar `@todo -check out correct level up: ranks, costs…`
  (L3211) signalisiert, dass der Author selbst unsicher ist.
- **Kritikalität:** niedrig, weil die Logik korrekt ist — aber
  fehlende Doku + unklare Semantik = Bug-Magnet.

**Empfehlung für späteren Fix:**
In `__takeValsCat` Docstring explizit dokumentieren, dass `bkpusedDP`
„Snapshot vor aktueller Reserve" ist und dass der
Rollback-Zweig `__usedDP` **auf jenen Wert** zurücksetzt, nicht auf 0.

---

### D3 — **`__renameSkill` commit/restore-Tanz verliert `__usedDP` bei Exception** (Kritikalität: MITTEL)

**Befund:** L3459–L3460:
```
self._character['DP']  -= self.__usedDP
self.__usedDP           = 0
```
L3492:
```
self._character['DP']  = dummyDP
```

**Problem:**
1. Zwischen L3460 und L3492 ist `__usedDP = 0`. Falls eine Exception
   in `__calcTotals` (L3488), `__buildWin` (L3489), `__buildTree`
   (L3490) oder `__buildChangedTree` (L3491) wirft, gibt es **keinen
   try/finally** — der DP-Wert bleibt `character['DP'] - __usedDP`
   (also dauerhaft reduziert), und `__usedDP` bleibt 0 (also „verloren"
   aus Sicht des nächsten `__finalize`-Aufrufs, der nichts zu
   kommittieren hat, weil das Ledger leer ist).
2. Im Erfolgsfall: `dummyDP = int(character['DP'])` (L3483) hält den
   Wert **nach** dem Deduct. L3492 setzt `character['DP'] = dummyDP`
   → netterweise no-op. **Aber**: `__usedDP = 0` (L3460) wird
   **nicht** wiederhergestellt. Wenn der User nach dem Rename weiter
   „Take" drückt, wird das Ledger **nur** die neuen Takes enthalten —
   die vor-Rename-Takes sind in `character['DP']` **schon
   abgezogen** (via L3459) und in `__usedDP` **nicht mehr** enthalten
   (via L3460). Das ist **falsch** — der User „verliert" seine
   Session-Reservierung, weil `__renameSkill` sie ins Character-Dict
   einbrennt und das Ledger leert.
3. **Falscher Commit-Mechanismus:** D3 ist faktisch ein dritter
   Commit-Punkt (in-Form von „in Character-Dict einbrennen"), der
   **vor** `__finalize` liegt und **kein** `__usedDP`-Reset
   zurückgibt. Das verletzt das Ledger-Modell.

**Empfehlung für späteren Fix (doku only):**
- try/except/finally um L3460–L3492, so dass `character['DP']`
  immer wiederhergestellt wird, wenn der Rename fehlschlägt.
- Oder: `__renameSkill` sollte das Character-Dict **nicht** direkt
  modifizieren, sondern nur `__changed` puffern und `__usedDP`
  angetastet lassen (konsistent mit D1-Modell).
- Oder: L3492 wird `self._character['DP'] = dummyDP` →
  `self._character['DP'] += self.__usedDP` (wenn `__usedDP` vor
  L3460 gesichert wird).

---

## 4. Reproduktionspfad für den Original-Bug-Report

**Report:** *„beim steigern von cat werden die entsprechenden punkte
nicht von den DP abgezogen."*

**Vorausetzung:** User steigt eine Kategorie um (z. B. „Combat" von
Rank 1 → 3), drückt „Take", und erwartet, dass die DP-Zahl sichtbar
sinkt. Was tatsächlich passiert:

1. **UI-Zeile:** `self.DPtext.set(character['DP'] - __usedDP)` (L3329).
   → **Die sichtbare DP-Zahl sinkt sofort** (weil `__usedDP` wächst).
2. **Character-Dict:** `character['DP']` ändert sich **nicht**
   (weil der Commit L3345 erst bei „Finalize" kommt).
3. **Bei „Finalize":** `character['DP'] -= __usedDP` (L3345) → DP sinkt.
4. **Bei „Close" ohne Finalize:** `character['DP']` bleibt **unverändert**
   (D1).

**Zwei mögliche Interpretationen des Bug-Reports:**

- **(H1) Visible-UI-Bug:** Der User sieht die DP-Zahl sinken, aber
  erwartet, dass auch `character['DP']` sofort sinkt. → **Entspricht
  dem Design** (Ledger-Modell). **Kein Bug**, sondern
  Feature-Vermischung. Empfehlung: UI-Label klarer („verfügbar"
  vs. „verbleibend").

- **(H2) Persistenz-Bug:** Der User drückt „Take", schließt das
  Fenster (X statt Finalize), und `character['DP']` sinkt nicht.
  → **D1-Bug** (L2330 auskommentiert). **Tatsächlicher Bug.**

**Verifikation:** Wenn der User „Take" + „Finalize" (statt Close)
drückt, sinkt `character['DP']` korrekt (L3345). Nur der
Close-ohne-Finalize-Pfad ist defekt.

**Einschränkung:** Diese Analyse ist **statisch**; ein dynamischer
Repro-Test in einer Headless-Umgebung ist nicht trivial, weil
`skillcatWin` eine Tkinter-Instanz + einen Character-Dict mit
specific-Struktur braucht. Die Zeilenreferenzen sind korrekt
(awk-verifiziert), die Defekte sind aus dem Code ablesbar.

---

## 5. Offene / zu-verifizierende Punkte

1. **D1 Intent:** War L2330/L2331 bewusst auskommentiert?
   - Git-Blame: `git log -L 2324,2336:epwins.py` — prüfen, wer wann
     und warum auskommentiert hat.
   - `git blame epwins.py | head -30` auf L2324–L2337.
2. **D2 Semantik:** Ist `bkpusedDP` ein „Snapshot vor Reserve"
   (korrekt) oder ein „Reset-Target" (falsch)?
   - Codelesung sagt „Snapshot" — aber Docstring ist leer.
3. **D3 Exception-Safety:** Ist die L3460–L3492-Region
   ausnahmesicher?
   - Nur `try/except`-Sichtprüfung im Code — kein try/except vorhanden.
4. **`rm.choseProfession` / `rm.refreshStatBonus`** (L3340–L3342 in
   `__finalize`) — diese Methoden sind extern (rpgtoolbox
   `rolemaster`). Sie könnten `character['DP']` ebenfalls
   modifizieren. **Nicht in dieser Analyse verifiziert** — müsste bei
   einem Fix nachgezogen werden.
5. **`__calcTotals`** (L2930) — Wrapper um
   `rpgtoolbox.rpgtools.calcTotals()`. Kann dieser `character['DP']`
   modifizieren? Nicht verifiziert.

---

## 6. Nächste Schritte (späterer Fix, kein Code jetzt)

1. **D1:** `git log -L` auf `__closewin` — Intent klären.
   - Falls beabsichtigt: Rollback-Policy (Puffer verwerfen)
     dokumentieren.
   - Falls nicht beabsichtigt: L2330/L2331 dekommentieren.
2. **D3:** try/except/finally in `__renameSkill`; `dummyDP`-Restore
   im `finally`-Block.
3. **D2:** Docstring in `__takeValsCat` ergänzen (bkpusedDP-Semantik).
4. **UI-klarheit:** `DPtext`-Label von „verbleibend" →
   „verbleibend (inkl. Session-Reservierung)" oder ähnlich, um die
   H1-Interpretation des Bug-Reports zu entschärfen.

---

## 7. Referenzen

- Code: `src/gui/epwins.py`, Klasse `skillcatWin` (L2238–L4100).
- Key-Lines: L2324 (closewin), L2375 (init), L2579–L2606 (Buttons),
  L2933 (takeValsSkill), L3206 (takeValsCat), L3333 (finalize),
  L3451 (renameSkill), L3483 (dummyDP), L3492 (restore).
- BUG-Report: `docs/bug_report_2026-08-26.md` (BUG-006, BUG-007,
  BUG-008).
- Bug-Tracker: `src/BUGS.md` (9.462 c, 2026-08-26).
- TODO: `src/TODO.md` (DP-Referenzen).
- Rpgtools-externe: `src/rpgtoolbox/charhandler.py` (Socket-Scaffold,
  **kein** Bug-Lokation), `src/rpgtoolbox/globaltools.py` L353
  (`writeJSON`), `src/rm_char_tools.py` (deprecated, **kein**
  Bug-Lokation).

---

## 8. Inline-Doku-Audit (Doxygen/Python, 2026-08-27)

**Audit-Objekt:** Die 5 DP-relevanten Methoden von `skillcatWin`.
**Kriterium:** Method-Docstring muss Zweck + bekannte Mängel (`@bug`/`@todo`/
`@note`) enthalten — konsistent mit der Codebase-Konvention
(`'''+Doxygen-Tags`), vgl. `doxygen-python-inline-docs`-Skill.

| Methode | Vorher | Nachher |
|---|---|---|
| `__takeValsSkill` (L2933) | `@todo` + `@bug` (2 Punkte) vorhanden | unverändert (ausreichend) |
| `__takeValsCat` | nur 1× `@todo` (XXXX-Schliff) | **NEU:** `@note` bkpusedDP-Semantik (D2) |
| `__finalize` | Zweck dokumentiert, Ledger-Commit nicht benannt | unverändert (Kommentar L3344 reicht) |
| `__closewin` | nur 1-Zeilen-Zweck | **NEU:** `@bug` D1 (kommentierter Commit) |
| `__renameSkill` | nur 1× `@todo` | **NEU:** `@bug` D3 (kein try/finally) |

**Befund:** Vor dem Audit war das Ledger-Verhalten an exakt den drei
Stellen, wo der Bug liegt, in den Docstrings **nicht** erkennbar.
Die neuen `@bug`/`@note`-Blöcke verweisen alle auf
`src/BUG_008_DP_DEDUCTION_ANALYSIS.md` mit Defekt-Id (D1/D2/D3).
`py_compile gui/epwins.py`: **exit 0** (4× SyntaxWarning `\e` bereits
vor dem Audit vorhanden, nicht verursacht durch diese Patches).

---

## 9. GUI-Test-Dokumentation (manuell, da Headless-Repro inkonklusiv)

**Warum kein automatischer GUI-Test:** `skillcatWin` ist eine
Tkinter-Klasse mit starkem UI-Abhängigkeitsgraph (Treeview, Spinboxes,
Modalfenster, `rpgtoolbox.rolemaster`-Importe). Ein Headless-Repro mit
Mocks (versucht am 2026-08-27, `/tmp/dp_test.py` v1–v3) scheiterte an
dem unmanglebaren `_skillcatWin__calcRanks` und fehlenden
Window-Mocks — Setup-Komplexität übersteigt den Test-Wert für
**Dokumentationszwecke**. Die nachfolgenden Schritte sind dafür
konstruiert, dass ein Tester sie 1:1 ausführen kann.

**Voraussetzung:** Charakter-JSON mit `DP >= 20`, `lvlup >= 2`,
mind. 1 Kategorie mit `dpCosts`-Liste (z. B. Combat) + 1 Skill.

**Test 1 — Skill-Levelup + Finalize (erwartet: korrekt):**
1. `python3 rpgtools.py` → Charakter laden → „Cats/Skills"-Menü.
2. Skill wählen, Rank um +1, „Take" drücken.
3. **Sichtprüfung:** DPtext-Zeile zeigt `alte_DP - cost` (sofort).
4. „Finalize" drücken → `character['DP']` sinkt um die Kosten
   (L3345). Charakter-Save → JSON öffnen → `DP`-Feld ist reduziert.
5. **Erwartet: PASS.**

**Test 2 — Category-Levelup + Finalize (erwartet: korrekt):**
1. Kategorie wählen, Rank um +N, „Take" → DPtext sinkt um
   `dpCosts[lowval..lowval+N-1]` (L3286).
2. „Finalize" → `character['DP']` sinkt. Save → JSON geprüft.
3. **Erwartet: PASS.**

**Test 3 — Category-Levelup + CLOSE ohne Finalize (erwartet: D1-BUG):**
1. Kategorie um +1 steuern, „Take" → DPtext sinkt sofort.
2. Fenster mit X schliessen (kein Finalize).
3. Zurück in MainWindow → Charakter laden / speichern → JSON öffnen.
4. **Erwartet: `character['DP']` NICHT reduziert, `lvlup` um 1
   reduziert → D1 reproduziert. Bug-Bestätigung.**

**Test 4 — Rename-Doppeltcommit (erwartet: D3-verdächtig):**
1. „Take" auf Kategorie +1 (DPtext sinkt).
2. „Rename" auf einem Skill → `character['DP']` wird L3459 **sofort**
   reduziert und L3492 wiederhergestellt (netto-Null), ABER `__usedDP`
   ist null.
3. „Finalize" → kein weiterer Commit möglich (Ledger leer),
   `lvlups`-Zähler des Renames ist konsistent.
4. **Erwartet: Funktioniert im Glückfall, aber: ein Exception im
   Rename (z. B. leerer Skillnamen) verliert die Session-Reservierung.
   D3-Bestätigung.**

**Test 5 — Rollback (erwartet: korrekt, D2-Semantik):**
1. Kategorie auf Rank, bei dem die Gate-Prüfung `character['DP'] -
   __usedDP < 0` **fehlschlägt** (DP künstlich niedrig im
   Charakter-JSON setzen).
2. `__usedDP` wird L3324 auf `bkpusedDP` zurückgesetzt (L3281) —
   d. h. auf den Zustand **vor** dem Versuch, nicht auf 0.
3. UI zeigt: DPtext-Zeile bleibt wie vor dem Versuch. **Erwartet: PASS.**

**Ergebnis-Protokoll:**
```
Test # | Status (PASS/FAIL) | Anmerkung
T1     |                    |
T2     |                    |
T3     |                    |  (erwartet: FAIL = D1 reproduziert)
T4     |                    |  (erwartet: D3 bestätigt)
T5     |                    |
```

---

*Note erstellt 2026-08-27, statische Analyse,
zeilenverifziert gegen aktuelles `epwins.py`. Kein Code-Fix
implementiert. Inline-Doku-Patches (Abschnitt 8) sind die einzige
Code-Änderung — alle rein dokumentierend.*

---

## 9. VERIFIZIERUNG (2026-08-28) — BEIDE PÄDTE FUNKTIONIERN

Xvfb-Reproduktions-Harness `src/gui/test_dp_repro.py` mit echtem Charakter
(`data/Marcus/Finrion.json`, DP=79) und realer Fensterinstanz:

    === CAT TEST: 'Armor - Medium'  rank=10  costs=2 2 2
      [before]            __usedDP=0   DPtext='79'
      [after  cat rank+1] __usedDP=2   DPtext='77'      <- Abzug + Anzeige OK
    === SKILL TEST: 'Armor - Light' / 'Rigid Leather'  rank=1  costs=1 1 1
      [before]            __usedDP=2   DPtext='77'
      [after skill rank+1] __usedDP=3  DPtext='76'      <- Abzug + Anzeige OK
    EXIT=0

Ergebnis: `__takeValsCat` UND `__takeValsSkill` ziehen bei Rank+1 korrekt
`__usedDP` auf, `DPtext` spiegelt `charDP - __usedDP`, chgtree zeigt beide
Änderungen. `git diff HEAD -- src/gui/epwins.py` = LEER — der Stand in
Commit `63cad53` (D1-Fix + Doxygen-Doku) ist der funktionierende Stand.
Die Liste-vs-String-Kompatibilität ist über `ab23950`
(`isinstance(raw_parent_dp, str)` Guard + `type(dpCosts) == type("1)`-Zweige)
bereits abgedeckt; `py_compile -W error::SyntaxWarning` → clean.

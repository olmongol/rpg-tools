# TODO - RPG Tools Feature- und Wartungsliste

## Attackcheck (src/attackcheck.py)

### [TODO-001] Konfigurationsfenster fuer Kampf-Ausstattung (HIGHER PRIORITY)
- **Stand:** Offener Todo aus Header-Kommentar ab Zeile 17
- **Pfad:** Konfigurations-Window fuer: Waffen, Krauter, Artefakte etc. fuer beide Kämpfer-Gruppen

### [TODO-002] Kraut-Nutzungs-Fenster (HIGHER PRIORITY)
- **Stand:** Offener Todo aus Header-Kommentar ab Zeile 19
- **Pfad:** Fenster zum Verwenden von Kraeutern waehrend des Kampfes mit Beschreibungsfunktion

### [TODO-003] EP-Logging fuer Kämpfe (HIGHER PRIORITY)
- **Stand:** Offener Todo aus Header-Kommentar ab Zeile 21
- **Pfad:** Treffer und Krits logger fuer EP-Berechnung nach Dateiausgabe

### [TODO-004] Munitions-Ressourcen logging (HIGHER PRIORITY)
- **Stand:** Offener Todo aus Header-Kommentar ab Zeile 22-23
- **Pfad:** Munitions-Ressourcen logging von NPC/PC → Speichern in Inventar

### [TODO-005] Schaeden an Charakterbogen schreiben (HIGHER PRIORITY)
- **Stand:** Offener Todo aus Header-Kommentar ab Zeile 24
- **Pfad:** Damage- und Modifier-Werte in den Charakterbogen speichern

---

## EP Calculator (src/epcalcwin.py/epcalc.py)

### [TODO-008] RR-Fenster hinzufuegen (HIGHER PRIORITY)
- **Stand:** Todo im Header ab Zeile 14
- **Pfad:** epcalc.py / existing rrwindow.py exists - check integration status

### [TODO-009] Gruppen-Skill-Checker (HIGHER PRIORITY)
- **Stand:** Todo im Header ab Zeile 15
- **Beschreibung:** Skill auswählen und für ganze Gruppe pruefen

### [TODO-010] Spellcasting-Fenster (HIGHER PRIORITY)
- **Stand:** Todo im Header ab Zeile 16; Button auf Zeile 237 zeigt noch `notdoneyet`
- **Beschreibung:** Eigentliches Spellcasting Window implementieren

---

## Findherbs (src/findherbs.py)

### [TODO-014] OptionMenu für Kraut-Zweck hinzufügen (HIGHER PRIORITY)
- **Stand:** Todo im SuchHerbsWin-Klassen docstring Zeile 254
- **Beschreibung:** Dropdown für das Verwendungszweck des gesuchten Krauts

### [TODO-015] Logger-Pfad config-basiert machen (MEDIUM PRIORITY)
- **Stand:** Hardcodiert `'./log/'` auf Zeile 38 → sollte chkCfg() nutzen wie andere Module

---

## Monster Creator (src/monstercreator.py)

### [TODO-016] GMtable Konfigurations-Fenster (HIGHER PRIORITY)
- **Stand:** Todo in monstercreatorWin ab Zeile 52: config window for NPC templates

### [TODO-017] Magic item properties - full implementations needed (MEDIUM)
- **Stand:** Mehrere `@todo` ab Zeilen 622, 631, 640, 648, 657
- **Pfad:** npc/monster item creation → magic properties

---

## rm_char_tools.py (Main Entry Point)

### [TODO-023] Design: individuelle/Gruppen-Historie + Kalender-Modul (MEDIUM PRIORITY)
- **Stand:** Todo im Header ab Zeile 21

### [TODO-024] Design: Krautlager und Suche (LOW PRIORITY)
- **Stand:** Todo im Header ab Zeile 22

---

## rm-inventory.py (Character Inventory)

### [TODO-030] Character Group Calculation - implement full (HIGHER PRIORITY)
- **Stand:** TODO ab 7× vorkommend, Zeilen 594, 1251, 1525, 1558, 1822, 3345, 4690

### [TODO-047] rm-inventory.py ist ~5058 Zeilen gross - Refactoring empfohlen (HIGHER PRIORITY)
- **Beschreibung:** Einzelne Klasse InventoryWin in kleinere Komponenten aufteilen. Das ist die laengste Datei im Projekt.

---

## rpgtoolbox Package

### [TODO-037] Calendar not fully implemented (MEDIUM PRIORITY)
- **Stand:** TODO auf Zeile 250 in calendar.py

### TODO-038: rmfight - full implementation (MEDIUM PRIORITY)
- **Stand:** TODO ab Zeilen 55, 64 in `rpgtoolbox/rmfight.py`
- **Beschreibung:** Kampfsystem für Role Master - mehrere TODOs als stub

---

## GUI Package (src/gui/)

### [TODO-041] epwins.py - skill level up validation (HIGHER PRIORITY)
- **Stand:** TODO "check out correct level up: ranks, costs etc." auf Zeile 3211

### [TODO-042] pic does not work 
- **Stand:** Bug-Kommentar "BUG pic does not work" in epwins.py und .bak Files um Zeile 3883
- **Beschreibung:** Charakterbild-Felder funktionieren nicht zuverlässig

---

## General / Architecture

### [TODO-044] Log-Pfade konsistent machen (HIGH PRIORITY for maintainability)
- **Stand:** findherbs.py Zeile 38 hat einen hardcodierten `'./log/'` Pfad; alle anderen verwenden chkCfg()

### [TODO-046] Codebase cleanup - remove dead/backup files (LOW PRIORITY)
- **Stand:** `attackcheck.py.bak`, `epwins.py.bak`, `epwins.py.bak3` (siehe auch BUG-007)

---

## BEREITS GEFIXT - NICHT MEHR AKTUELL

| TODO | Status | Details |
|------|--------|---------|
| TODO-006 | ✅ FIXED | Debug prints in attackcheck.py wurden entfernt |
| TODO-007 | ✅ FIXED | Duplicate import randint wurde bereinigt |
| TODO-013 | ✅ FIXED | foundherbs.py bug (None → []) gefixt |
| TODO-022 | ✅ FIXED | print(os.getcwd()) in monstercreator.py entfernt |
| TODO-045 | ✅ GECHECKT | 2026-08-28: alle 21 LANCZOS-Stellen in gui/ bereits `Resampling.LANCZOS`, kein nacktes `Image.LANCZOS` übrig |
